import yfinance as yf
import requests
import argparse
from typing import Callable, Dict, List

DEFAULT_WEBHOOK_URL: str = (
    "https://discord.com/api/webhooks/1364281346318401717/UURBuuOz_sOV5F3FItjCBvzSI3-NBeLpuVaUTyBT3H1Kb09frxZbJnEY7RdWBOXNI9kW"
)


def emil_coecus() -> str:
    spy_ticker = yf.Ticker("SPY")  # SPY price in USD
    ussp = spy_ticker.fast_info["lastPrice"]

    # Get EUR/USD exchange rate and convert to USD/EUR
    eur_usd_ticker = yf.Ticker("EURUSD=X")
    eur_usd = eur_usd_ticker.fast_info["lastPrice"]
    eur = 1 / eur_usd

    sp = eur * ussp  # Calculate SPY price in EUR

    # Reference values
    spstart = 474.077
    dsp = sp - spstart
    spread = spstart * 0.05
    # cap = spstart + spread
    # floor = spstart + spread  # Note: same as cap in original

    # Bet parameters
    bet = 40
    rate = 2

    # Calculate winnings
    if dsp > 0:
        win = min(dsp * bet / spread, bet)
        winner = "Emil"
    else:
        win = min(-dsp * bet * rate / spread, bet * rate)
        winner = "Coecus"

    message = f"v Coecus: {winner} is winning by {round(win, 2)}€ because of a {(dsp/spstart)*100:.2f}% shift in S&P 500 [EUR] ({spstart} -> {sp:.2f})\n"
    return message


def emil_smoid() -> str:
    # Get EUR/USD exchange rate and convert to USD/EUR
    eur_usd_ticker = yf.Ticker("EURUSD=X")
    eur_czk_ticker = yf.Ticker("EURCZK=X")
    eur_usd = eur_usd_ticker.fast_info["lastPrice"]
    eur_czk = eur_czk_ticker.fast_info["lastPrice"]

    # Reference values
    eur_usd_start = 1.1476
    deur = eur_usd - eur_usd_start
    win = deur * 3000

    # Calculate winnings
    if win > 0:
        winner = "Šmoid"
    else:
        winner = "Emil"

    message = f"v Šmoid: {winner} is winning by {round(abs(win), 2)}€ (payout {round(abs(win) * eur_czk, 2)} Kč) because of a {(deur/eur_usd_start)*100:.2f}% shift ({eur_usd_start:.3f} -> {eur_usd:.3f})\n"
    return message


def post_discord(msg: str, webhook_url: str) -> None:
    payload = {"content": msg}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Successfully posted to Discord")
    except requests.exceptions.RequestException as e:
        print(f"Failed to post to Discord: {e}")


AVAILABLE_BETS: Dict[str, Callable[[], str]] = {
    "coecus": emil_coecus,
    "smoid": emil_smoid,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate and report on various financial bets.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--webhook-url",
        default=DEFAULT_WEBHOOK_URL,
        help="The Discord webhook URL to post results to.",
    )

    parser.add_argument(
        "--no-post",
        dest="post_to_discord",
        action="store_false",
        help="Disable posting the message to Discord. Prints to stdout only.",
    )

    bet_choices = list(AVAILABLE_BETS.keys()) + ["all", "none"]
    parser.add_argument(
        "--bets",
        nargs="+",
        choices=bet_choices,
        default="all",
        help=(
            "Which bets to run. Can be one or more bet names or a keyword.\n"
            "'all': (default) runs all available bets.\n"
            "'none': runs no bets.\n"
            f"Available bets: {', '.join(AVAILABLE_BETS.keys())}"
        ),
    )

    args = parser.parse_args()

    if "none" in args.bets:
        args.bets = []
    elif "all" in args.bets:
        args.bets = list(AVAILABLE_BETS.keys())

    messages: List[str] = []
    print(args)
    for bet_name in args.bets:
        bet_function = AVAILABLE_BETS[bet_name]
        try:
            messages.append(bet_function())
        except Exception as e:
            messages.append(f"Error calculating bet '{bet_name}': {e}\n")

    final_message = "".join(messages)
    print(final_message, end="")

    if args.post_to_discord:
        post_discord(final_message, args.webhook_url)


if __name__ == "__main__":
    main()
