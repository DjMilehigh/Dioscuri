from playwright.sync_api import Page, expect

def test_chat_ui(page: Page):
    page.goto("http://localhost:8501")

    expect(page.get_by_text("Dioscuri")).to_be_visible()

    expect(page.get_by_text("Settings")).to_be_visible()
    expect(page.get_by_text("Temperature")).to_be_visible()
    expect(page.get_by_text("Enable Jailbreak")).to_be_visible()
    expect(page.get_by_text("Clear Chat")).to_be_visible()

    page.get_by_label("Enter your message:").fill("Hello")
    page.get_by_label("Enter your message:").press("Enter")

    expect(page.get_by_text("user")).to_be_visible()
    expect(page.get_by_text("Hello")).to_be_visible()

    page.screenshot(path="jules-scratch/verification/verification.png")
