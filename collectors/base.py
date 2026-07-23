from playwright.sync_api import sync_playwright
import time


class ColetorBase:

    def obter_html(self, url, seletor=None, timeout=60000):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page(
                viewport={
                    "width": 1366,
                    "height": 768
                },
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "Chrome/120 Safari/537.36"
                )
            )

            print(f"Acessando: {url}")

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=timeout
            )

            # aguarda scripts carregarem
            time.sleep(10)

            if seletor:

                try:
                    page.wait_for_selector(
                        seletor,
                        timeout=20000,
                        state="attached"
                    )

                    print(
                        f"Seletor encontrado: {seletor}"
                    )

                except Exception:

                    print(
                        f"Aviso: seletor não encontrado: {seletor}"
                    )


            html = page.content()


            # salva para análise
            with open(
                "pagina_debug_playwright.html",
                "w",
                encoding="utf-8"
            ) as f:
                f.write(html)


            browser.close()

            return html