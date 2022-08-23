import typer
import random
import httpx
import time
import rich
from rich.progress import Progress,SpinnerColumn, TextColumn
from rich.console import Console
from rich.table import Table
import threading
import yfinance as yf
import mplfinance as mpf
import json
from datetime import datetime
import pandas as pd
from prettytable.colortable import ColorTable,Themes
from prettytable import ALL
###################################

app = typer.Typer(rich_markup_mode="rich",help="[italic]It's an open-source tool that uses [green]Yahoo's[/green] publicly available APIs,and is intended for [red]research[/red] and [red]educational[/red] purposes.[/italic]")

views = ['trending-tickers','most-active','gainers','losers']

@app.command(help="[bold yellow]Show the markets.[/bold yellow]")
def markets(view:str = typer.Argument(...,help="[italic blue]'trending-tickers','most-active','gainers','losers'[/italic blue]")):
    if view not in views:
        rich.print(f"[red]Error: unrecognized arguments [bold]'{view}'[/bold]. The view should be [blue]'trending-tickers', 'most-active','gainers','losers'[/blue].[/red]")
        typer.Exit()
    else:
        def main():
            url = f'https://yfinance-stocks.deta.dev/{view}'
            data = httpx.get(url).json()
            for dt in data:
                for k,v in dt.items():
                    x = ' ' * (10 - len(k) + 2)
                    rich.print(f'[bold blue]{k}[/bold blue]{x}[yellow]{v}[/yellow]')
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
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
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
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized interval:[bold]'{interval}'[/bold][/yellow]")
            typer.Exit()
        else:
            ticker = yf.Ticker(market.upper())
            hist = ticker.history(interval=interval)
            if hist.empty:
                rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
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

@app.command(help="[bold yellow]Show actions (dividends, splits).[/bold yellow]")
def actions(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]")):
    def main():
        ticker = yf.Ticker(market.upper())
        df = ticker.actions.reset_index()
        if df.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            console = Console()
            table = Table("Date", "Dividends","Stock Splits")
            for index, row in df.iterrows():
                table.add_row(str(row['Date']),str(row['Dividends']),str(row['Stock Splits']),end_section=True)
            console.print(table)
    def spinner():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Processing...", total=None)
            time.sleep(0.5)
    t1 = threading.Thread(target=main, args=())
    t2 = threading.Thread(target=spinner, args=())
    t1.start()
    t2.start()
    t1.join()

@app.command(help="[bold yellow]Show splits.[/bold yellow]")
def splits(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]")):
    def main():
        ticker = yf.Ticker(market.upper())
        df = ticker.splits.reset_index()
        if df.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            console = Console()
            table = Table("Date","Stock Splits")
            for index, row in df.iterrows():
                table.add_row(str(row['Date']),str(row['Stock Splits']),end_section=True)
            console.print(table)
    def spinner():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Processing...", total=None)
            time.sleep(0.5)
    t1 = threading.Thread(target=main, args=())
    t2 = threading.Thread(target=spinner, args=())
    t1.start()
    t2.start()
    t1.join()

@app.command(help="[bold yellow]Show financials.[/bold yellow]")
def finance(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]"),quater:bool = typer.Option(default=False,help="get quarterly financials")):
    def main():
        ticker = yf.Ticker(market.upper())
        df = ticker.history()
        if df.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            # Create a dataframe (we can't use this `df` DataFrame because of column names are change)
            df = ticker.financials.reset_index() if quater else ticker.quarterly_financials.reset_index()
            # DataFrame -> Json -> Dict
            data = json.loads(df.to_json())
            # Create `headers` List & `finance` Dict
            headers, finance = ['Attribute'], {}
            # Update `headers` List or Loop `data` keys
            for key in data.keys():
                if key.endswith('000'):
                    key = int(key)
                    key /= 1000
                    headers.append(datetime.utcfromtimestamp(int(key)).strftime('%Y-%m-%d'))
            # _____Optinal______
            # Declare and Initialize variable `i`
            i = 0
            # Loop `data` values 
            for value in data.values():
                dt = []
                for val in value.values():
                    dt.append(str(val))
                finance.update({headers[i]:dt})
                i+=1
            # Override `df` variable 
            df = pd.DataFrame(finance)
            # _____Optinal_______
            # Create `console` instance 
            console = Console()
            # Create a table instance 
            table = Table(headers[0],headers[1],headers[2],headers[3],headers[4])
            # Loop `df` DateFrame
            for index, row in df.iterrows():
                table.add_row(str(row[headers[0]]),str(row[headers[1]]),str(row[headers[2]]),str(row[headers[3]]),str(row[headers[4]]),end_section=True)
            # rich.print Rich's table
            console.print(table)
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

@app.command(help="[bold yellow]Show major holders.[/bold yellow]")
def holders(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]")):
    def main():
        ticker = yf.Ticker(market.upper())
        # Declare and Initialize `df:DataFrame`
        df = ticker.major_holders
        if df.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            # Declare and Initialize `header:List`
            header = df.columns.values.tolist()
            # Create `console` instance 
            console = Console()
            # Create a table instance 
            table = Table(str(header[0]),str(header[1]))
            # Loop `df` DateFrame
            for index, row in df.iterrows():
                table.add_row(str(row[header[0]]),str(row[header[1]]),end_section=True)
            # rich.print Rich's table
            console.print(table)
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

@app.command(help="[bold yellow]Show institutional holders.[/bold yellow]")
def institutional_holders(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]")):
    def main():
        ticker = yf.Ticker(market.upper())
        # Declare and Initialize `df:DataFrame`
        df = ticker.institutional_holders
        if df.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            # Declare and Initialize `header:List`
            header = df.columns.values.tolist()
            # Create `console` instance 
            console = Console()
            # Create a table instance 
            table = Table(str(header[0]),str(header[1]),str(header[2]),str(header[3]),str(header[4]))
            # Loop `df` DateFrame
            for index, row in df.iterrows():
                table.add_row(str(row[header[0]]),str(row[header[1]]),str(row[header[2]]),str(row[header[3]]),str(row[header[4]]),end_section=True)
            # rich.print Rich's table
            console.print(table)
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

@app.command(help="[bold yellow]Show balance sheet.[/bold yellow]")
def balance_sheet(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]"),quater:bool = typer.Option(default=False,help="get quarterly balance_sheet")):
    def main():
        # Declare and Initialize `ticker` instance 
        ticker = yf.Ticker(market.upper())
        hist = ticker.history()
        if hist.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            # Declare and Initialize `df` DataFrame According to the condition
            df = ticker.quarterly_balance_sheet.reset_index() if quater else ticker.balance_sheet.reset_index()
            # Declare and Initialize `headers` and `rows` Lists
            headers, rows = df.columns.values.tolist(), []
            # Declare and Initialize `table` instance
            table = ColorTable(theme=Themes.OCEAN)
            # Set table header 
            table.field_names = headers
            # Set borders 
            table.hrules = ALL
            # Set table rows 
            for index,row in df.iterrows():
                table.add_row([row[headers[i]] for i in range(len(row))])
            # Print table 
            print(table)
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

@app.command(help="[bold yellow]Show cashflow.[/bold yellow]")
def cashflow(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]"),quater:bool = typer.Option(default=False,help="get quarterly cashflow")):
    def main():
        # Declare and Initialize `ticker` instance 
        ticker = yf.Ticker(market.upper())
        hist = ticker.history()
        if hist.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            # Declare and Initialize `df` DataFrame According to the condition
            df = ticker.quarterly_cashflow.reset_index() if quater else ticker.cashflow.reset_index()
            # Declare and Initialize `headers` and `rows` Lists
            headers, rows = df.columns.values.tolist(), []
            # Declare and Initialize `table` instance
            table = ColorTable(theme=Themes.OCEAN)
            # Set table header 
            table.field_names = headers
            # Set borders 
            table.hrules = ALL
            # Set table rows 
            for index,row in df.iterrows():
                table.add_row([row[headers[i]] for i in range(len(row))])
            # Print table 
            print(table)
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

@app.command(help="[bold yellow]Show earnings.[/bold yellow]")
def earning(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]"),quater:bool = typer.Option(default=False,help="get quarterly cashflow")):
    def main():
        # Declare and Initialize `ticker` instance 
        ticker = yf.Ticker(market.upper())
        hist = ticker.history()
        if hist.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            # Declare and Initialize `df` DataFrame According to the condition
            df = ticker.quarterly_earnings.reset_index() if quater else ticker.earnings.reset_index()
            # Declare and Initialize `headers` and `rows` Lists
            headers, rows = df.columns.values.tolist(), []
            # Declare and Initialize `table` instance
            table = ColorTable(theme=Themes.OCEAN)
            # Set table header 
            table.field_names = headers
            # Set borders 
            table.hrules = ALL
            # Set table rows 
            for index,row in df.iterrows():
                table.add_row([row[headers[i]] for i in range(len(row))])
            # Print table 
            print(table)
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

@app.command(help="[bold yellow]Show sustainability.[/bold yellow]")
def sustainability(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]")):
    def main():
        # Declare and Initialize `ticker` instance 
        ticker = yf.Ticker(market.upper())
        hist = ticker.history()
        if hist.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            # Declare and Initialize `df` DataFrame
            df = ticker.sustainability.reset_index()
            # Declare and Initialize `headers` and `rows` Lists
            headers, rows = df.columns.values.tolist(), []
            # Declare and Initialize `table` instance
            table = ColorTable(theme=Themes.OCEAN)
            # Set table header 
            table.field_names = headers
            # Set borders 
            table.hrules = ALL
            # Set table rows 
            for index,row in df.iterrows():
                table.add_row([row[headers[i]] for i in range(len(row))])
            # Print table 
            print(table)
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

@app.command(help="[bold yellow]Show analysts recommendations.[/bold yellow]")
def recommendations(market:str = typer.Argument(...,help="[italic blue]Enter required market[/italic blue]")):
    def main():
        ticker = yf.Ticker(market.upper())
        # Declare and Initialize `df:DataFrame`
        hist = ticker.history()
        if hist.empty:
            rich.print(f"[yellow][bold]Sorry[/bold] ,unrecognized market:[bold]'{market}'[/bold][/yellow]")
            typer.Exit()
        else:
            # Declare and Initialize `df` DataFrame
            df = ticker.recommendations.reset_index()
            # Declare and Initialize `header:List`
            header = df.columns.values.tolist()
            # Create `console` instance 
            console = Console()
            # Create a table instance 
            table = Table(str(header[0]),str(header[1]),str(header[2]),str(header[3]),str(header[4]))
            # Loop `df` DateFrame
            for index, row in df.iterrows():
                table.add_row(str(row[header[0]]),str(row[header[1]]),str(row[header[2]]),str(row[header[3]]),str(row[header[4]]),end_section=True)
            # rich.print Rich's table
            console.print(table)
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


if __name__ == "__main__":
    app()
