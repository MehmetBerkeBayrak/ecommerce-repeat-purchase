
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from musteri_sorgula import musteri_sorgula


class MusteriAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            sayfa = Path(__file__).with_name("index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(sayfa)))
            self.end_headers()
            self.wfile.write(sayfa)
            return
        on_ek = "/api/musteri/"

        if not self.path.startswith(on_ek):
            return self.json_gonder(404, {"hata": "Adres bulunamadi."})

        kimlik = self.path[len(on_ek):]

        if not kimlik.isascii() or not kimlik.isdigit():
            return self.json_gonder(
                400, {"hata": "Musteri kimligi yalnizca rakam olmali."}
            )

        sonuc = musteri_sorgula(int(kimlik))
        durum = 404 if "hata" in sonuc else 200
        self.json_gonder(durum, sonuc)

    def json_gonder(self, durum, veri):
        govde = json.dumps(veri, ensure_ascii=False).encode("utf-8")
        self.send_response(durum)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(govde)))
        self.end_headers()
        self.wfile.write(govde)


if __name__ == "__main__":
    print("API: http://127.0.0.1:8001/api/musteri/17850")
    HTTPServer(("127.0.0.1", 8001), MusteriAPI).serve_forever()