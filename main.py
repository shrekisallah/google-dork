from colorama import Fore
import requests
from bs4 import BeautifulSoup


def main():
    cli = input(f'''{Fore.BLUE}Cli or json config? ''')
    if cli == cli:
        dork = input(f'''{Fore.BLUE}Enter a dork to use (default is intitle:”index of/” “cfdb7_uploads”):{Fore.RESET} ''')
        save = input(f'''{Fore.CYAN}Would you like to save to a file?: {Fore.RESET}''')
        rmdupe = input(f'''{Fore.CYAN}Would you like to remove duplicate results?: {Fore.RESET}''')
        pages = input(f'''{Fore.CYAN}How many pages would you like to search?: {Fore.RESET}''')
        thing = input(f'''{Fore.CYAN}Overwrite results file? {Fore.RESET}''')
        delay = input(f'''{Fore.CYAN}Delay between requests(in seconds): ''')
    try:
        pages = int(pages)
    except ValueError:
        print(f'''{Fore.RED}[!] {Fore.RESET}Invalid input, defaulting to 100 pages''')
        pages = 100
    if save == 'y' or save == 'Y' or save == 'yes' or save == 'Yes' or save == 'YES':
        save = True
    if thing == 'y' or save == 'Y' or save == 'yes' or save == 'Yes' or save == 'YES':
        with open('results.txt', 'r') as f:
            f.truncate(0)
    if dork == '':
        dork = 'intitle:”index of/” “cfdb7_uploads”'
    print(f'''{Fore.GREEN}[+]{Fore.RESET} Dork: {dork}''')
    print(f'''{Fore.GREEN}[+]{Fore.RESET} Searching...''')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    for a in range(pages):
        url = f'https://www.google.com/search?q={dork}&start={a * 10}'
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            thing = soup.find_all('a')
            for i in thing:
                if 'https://' in i.get('href') and 'google' not in i.get('href'):
                    temp = i.get('href')
                    temp = temp.split('=')
                    temp = temp[1]
                    temp = temp.split('&')
                    result = temp[0]
                    print(f'''{Fore.GREEN}[+]{Fore.RESET} Found: {result}''')
                    if save:
                        with open('results.txt', 'a') as f:
                            f.write(f'{result}\n')
                    sleep(delay)
        if r.status_code == 429:
            print(f'''{Fore.RED}[!] Ratelimited!{Fore.RESET}''')
        else:
            print(f'''{Fore.RED}[!]{Fore.RESET} Something went wrong! {Fore.RED}Error Code: {r.status_code}''')
    if rmdupe == 'y' or rmdupe == 'Y' or rmdupe == 'yes' or rmdupe == 'Yes' or rmdupe == 'YES':
        print(f'''{Fore.GREEN}[+]{Fore.RESET} Removing duplicates...''')
        dupes = 0
        with open('results.txt', 'r') as f:
            lines = f.readlines()
        with open('results.txt', 'w') as f:
            for line in lines:
                if line not in lines[lines.index(line)+1:]:
                    f.write(line)
                else:
                    dupes += 1
        print(f'''{Fore.GREEN}[+]{Fore.RESET} Removed {dupes} duplicates''')
    with open('results.txt', 'r') as f:
        lines = f.readlines()
    print(f'''{Fore.GREEN}[+]{Fore.RESET} Finished!''')


if __name__ == '__main__':
    main()
