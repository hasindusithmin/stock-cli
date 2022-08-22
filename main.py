import typer
import random
import httpx
import time
from rich import print
from rich.progress import Progress,SpinnerColumn, TextColumn
from rich.console import Console
from rich.table import Table
import threading
import yfinance as yf
import mplfinance as mpf
###################################

app = typer.Typer(rich_markup_mode="rich",help="[italic]It's an open-source tool that uses [green]Yahoo's[/green] publicly available APIs,and is intended for [red]research[/red] and [red]educational[/red] purposes.[/italic]")

views = ['trending-tickers','most-active','gainers','losers']

@app.command(help="[bold yellow]Fetches the market.[/bold yellow]")
def fetch(view:str = typer.Argument(...,help="[italic blue]'trending-tickers','most-active','gainers','losers'[/italic blue]")):
    if view not in views:
        print(f"[red]Error: unrecognized arguments [bold]'{view}'[/bold]. The view should be [blue]'trending-tickers', 'most-active','gainers','losers'[/blue].[/red]")
        typer.Exit()
    else:
        def main():
            url = f'https://yfinance-stocks.deta.dev/{view}'
            data = httpx.get(url).json()
            for dt in data:
                for k,v in dt.items():
                    x = ' ' * (10 - len(k) + 2)
                    print(f'[bold blue]{k}[/bold blue]{x}[yellow]{v}[/yellow]')
        def spinner():
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Processing...", total=None)
                time.sleep(2)
        t1 = threading.Thread(target=main, args=())
        t2 = threading.Thread(target=spinner, args=())
        t1.start()
        t2.start()
        t1.join()
    
@app.command(help="[bold yellow]Get stock information.[/bold yellow]")
def info(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]")):
    def main():
        ticker = yf.Ticker(market.upper())
        info = ticker.info
        exist = True if info['regularMarketPrice'] != None else False
        if exist:
            console = Console()
            table = Table("Name", "Value")
            for k,v in info.items():
                table.add_row(k,str(v),end_section=True)
            console.print(table)
        else:
            print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
    def spinner():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Processing...", total=None)
            time.sleep(5)
    t1 = threading.Thread(target=main, args=())
    t2 = threading.Thread(target=spinner, args=())
    t1.start()
    t2.start()
    t1.join()

@app.command(help="[bold yellow]Get historical market data.[/bold yellow]")
def chart(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]"),interval:str = typer.Option(default="1d",help="[italic blue]Enter required timeframe(5m,15m,30m,1h,1d)[/italic blue]")):
    def main():
        intervals = ['5m','15m','30m','1h','1d']
        valid_interval = True if interval in intervals else False
        if not valid_interval:
            print(f"[yellow][bold]Sorry[/bold] ,unrecognized interval:[bold]'{interval}'[/bold][/yellow]")
            typer.Exit()
        else:
            ticker = yf.Ticker(market.upper())
            hist = ticker.history(interval=interval)
            if hist.empty:
                print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
                typer.Exit()
            else:
                del hist['Dividends']
                del hist['Stock Splits']
                mpf.plot(hist,type="candle",style="yahoo",volume=True,title=f"{market}@{interval}")
    def spinner():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Processing...", total=None)
            time.sleep(2)
    t1 = threading.Thread(target=main, args=())
    t2 = threading.Thread(target=spinner, args=())
    t1.start()
    t2.start()
    t1.join()



if __name__ == "__main__":
    app()
