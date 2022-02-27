# Datové typy a jednotky

V následující tabulce jsou popsány všechny data v databázi, jejich jména v češtině, jejich jména v programu, jednotka a
datový typ.

| Název hodnoty    | Název v programu | Jednotka                | Datový typ   |
|------------------|------------------|-------------------------|--------------|
| Index            | `datetime`       | datum                   | `datetime64` |
| Venkovní teplota | `out_temp`       | °C                      | `float64`    |
| Venkovní vlhkost | `out_humidity`   | %                       | `float64`    |
| Rosný bod        | `dew_point`      | °C                      | `float64`    |
| Rychlost větru   | `wind_speed`     | m/s                     | `float64`    |
| Směr větru       | `wind_dir`       | anglická světová strana | `string`     |
| Nárazy větru     | `gust`           |                         | `float64`    |
| Tlak             | `bar`            | hPa                     | `float64`    |
| Srážky           | `rain_data`      | mm                      | `float64`    |

:::{hint}

Proměnné mají datový typ `float64` místo `int`, protože všechny obsahují {abbr}`NaN (Not a Number)` hodnoty.
:::