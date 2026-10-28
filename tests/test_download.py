import http.server
import socketserver
import threading

import pytest

from veo.download import download_file

PAYLOAD = bytes(range(256)) * 400  # 102,400 bytes


class FlakyRangeHandler(http.server.BaseHTTPRequestHandler):
    """Serves PAYLOAD with Range support; the first GET is cut off halfway."""

    requests: list[str] = []

    def log_message(self, *args):
        pass

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Length", str(len(PAYLOAD)))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()

    def do_GET(self):
        range_header = self.headers.get("Range")
        type(self).requests.append(range_header or "full")
        start = int(range_header.split("=")[1].rstrip("-")) if range_header else 0
        body = PAYLOAD[start:]
        self.send_response(206 if range_header else 200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if len(type(self).requests) == 1:
            self.wfile.write(body[: len(body) // 2])
            self.wfile.flush()
            self.connection.shutdown(2)  # drop the connection mid-transfer
            return
        self.wfile.write(body)


@pytest.fixture
def server():
    FlakyRangeHandler.requests = []
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), FlakyRangeHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}/file.bin"
    httpd.shutdown()
    httpd.server_close()


def test_download_resumes_after_dropped_connection(server, tmp_path, monkeypatch):
    monkeypatch.setattr("veo.download.time.sleep", lambda seconds: None)
    target = download_file(server, tmp_path / "file.bin")
    assert target.read_bytes() == PAYLOAD
    assert FlakyRangeHandler.requests[0] == "full"
    assert FlakyRangeHandler.requests[1].startswith("bytes=")
    assert not (tmp_path / "file.bin.part").exists()


def test_existing_file_is_not_downloaded_again(tmp_path):
    target = tmp_path / "file.bin"
    target.write_bytes(b"done")
    assert download_file("http://invalid.example/never", target).read_bytes() == b"done"
