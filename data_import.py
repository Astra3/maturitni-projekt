# tento soubor je odkázán v dokumentaci, první řádek je přeskočen
from Pocasi.core.imp import LegacyImport, EditData, data_imp

df_old = LegacyImport.old_import("Base data/total 2011-2018.csv")
df_old2 = LegacyImport.old_import("Base data/total 2018-2021.csv", is_iso8601=False, ambiguous_localize="NaT")
df_new = data_imp("Base data/2021.txt")
old = EditData(df_old)
old.combine(df_old2)
rainfall = old.rainfall(True)

new = EditData(df_new)
rain = EditData(rainfall)
rain.combine(new.rainfall(drop_rain=False))
new.combine(old.df)

df = new.df
rainfall = rain.df
# new.to_feather()
# rain.to_feather()
