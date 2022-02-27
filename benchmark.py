import time

from pocasi import pocasi_data
from pocasi.core.imp import imp
from pocasi.core.request import DataRequest, Graph

total_time = 0


def timer(func):
    def wrapper():
        global total_time
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        execution_time = end - start
        total_time += execution_time
        print(f"Čas testu: {execution_time} s\n")

    return wrapper


@timer
def filter_test():
    """Udělá jednoduchý filtr na venkovní teplotu pro všechny teploty větší než 5"""
    _ = pocasi_data[pocasi_data["out_temp"] > 5]


@timer
def math_test():
    """Provede výpočty na všech sloupcích DtaFrame (mimo sloupce wind_dir)."""
    data = pocasi_data.drop(columns=["wind_dir"])
    _ = data * 5 / 10
    _ = data / 10 * 5 + 8 - 9


@timer
def daily_summary_test():
    """Provede denní souhrn celé databáze."""
    data = DataRequest(None)
    _ = data.daily_summary()


@timer
def graph_test():
    """Vytvoří graf denního souhrnu."""
    graf = Graph(None)
    graf.daily_temp()


@timer
def imp_test():
    """Naimportuje data z .feather formátu."""
    _ = imp()


if __name__ == '__main__':
    print("Test filtrů...")
    filter_test()

    print("Test výpočtů...")
    math_test()

    print("Test denních souhrnů...")
    daily_summary_test()

    print("Test grafů...")
    graph_test()

    print("Import test...")
    imp_test()

    print(f"Celkový čas testů: {total_time}")
