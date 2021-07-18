import argparse
import requests
from bs4 import BeautifulSoup

VERSION = "0.0.0"


parser = argparse.ArgumentParser(
	description=f"steamer - Find steam games meant for you | v{VERSION}"
)
parser.add_argument(
	"-s", help="Specify minimum discount percentage [Default : 0]", type=int
)
parser.add_argument(
	"-p", help="Specify maximum game price [Default : infinite]", type=int
)
parser.add_argument(
	"-g", help='Search term(s) seperated by ", " [Default : None]', type=str
)
parser.add_argument(
	"-q", help='Maximum number of search results [Default : 50]', type=int
)
parser.add_argument("-t", help="Specify timeout [Default : 20]", type=int)
parser.add_argument("-v", help="Prints version", action="store_true")
parser.set_defaults(s=0, g="", q=50, t=20)

args = parser.parse_args()
sale = args.s
if args.p is not None:
	if args.p == 0:
		price = "free"
	else:
		price = args.p
else:
	price = "infinite"
terms = args.g.split(", ")
results_left = args.q
timeout = args.t
vers = args.v


if vers:
	print(f"steamer | {VERSION}")
	exit()

if sale < 0 or sale > 100:
	print("Please provide a valid discount percentage (integer between 0 and 100).")
	exit()

if price != "infinite" and price != "free" and price is not None and price < 0:
	print("Please provide a valid sale percentage (integer greater than or equal to 0).")
	exit()

if results_left < 0:
	print(
		"Please provide a valid number for search results "
		"(integer greater than or equal to 0)."
	)
	exit()

if timeout < 0:
	print("Please provide a valid timeout value (integer greater than or equal to 0).")
	exit()


searches_url = []
main_url = (
	"https://store.steampowered.com/search/"
	f"?maxprice={price}&specials={1 if sale > 0 else 0}&term="
)


def banner():
	banner = r"""
_____ _____ _____   _    _  _  _  _____ _____
|____   |   |____  /_\  | \/ \/ | |____ |___|
_____|  |   |____ /   \ |       | |____ |   \
	"""
	print(banner)
	print("[>] Created By : @BenVN123")
	print(f"[>] Version    : {VERSION}\n\n")


def make_search_urls():
	global searches_url
	if len(terms) == 0:
		searches_url.append(main_url)
		return
	else:
		for term in terms:
			searches_url.append(main_url + term)


def query(link, num):
	global results_left
	try:
		source = requests.get(link).text
	except requests.exceptions.ConnectionError:
		print("Failed to connect to Steam. Please check your network.")
		exit()
	dem_games = BeautifulSoup(source, "lxml").find(
		"div", attrs={"id": "search_resultsRows"}
	).find_all("a")

	i = 0
	rounds = 0
	while i < num:
		rounds += 1
		if len(dem_games) == 0 or rounds - i > num // 2:
			break

		a = dem_games[0]
		g_name = a.find("span", attrs={"class": "title"}).text.rstrip().lstrip()
		g_release = a.find(
			"div", attrs={"class": "col search_released responsive_secondrow"}
		).text.rstrip().lstrip()
		g_sale = a.find(
			"div", attrs={"class": "col search_discount responsive_secondrow"}
		).text.rstrip().lstrip()
		g_link = a["href"]

		if len(g_release) == 0:
			g_release = "?"
		
		if len(g_sale) == 0:
			if sale != 0:
				dem_games.pop(0)
				continue
			g_price = a.find(
				"div", attrs={"class": "col search_price responsive_secondrow"}
			).text.rstrip().lstrip().split("$")[-1]
		else:
			if float(g_sale[1:-1]) < sale:
				dem_games.pop(0)
				continue
			g_price = a.find(
				"div", attrs={"class": "col search_price discounted responsive_secondrow"}
			).text.rstrip().lstrip().split("$")[-1]

		da_game = (
			f"{g_price} "
			f"({'No Discount' if len(g_sale) == 0 else g_sale}) "
			f"- {g_name} | Released {g_release} | {g_link}\n"
		)

		if (
			len(g_price) == 0 or
			(price == "free" and g_price.lower() != "free to play" and
				g_price.lower() != "free"
				) or (price != "free" and price != "infinite" and float(g_price[1:]) > price)
		):
			dem_games.pop(0)
			continue

		dem_games.pop(0)
		print("[+]", da_game)

		i += 1
		results_left -= 1


def main():
	banner()
	make_search_urls()
	for url in searches_url:
		query(url, results_left // len(terms) if len(terms) > 0 else 1)


main()
