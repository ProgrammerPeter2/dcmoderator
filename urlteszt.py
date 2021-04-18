import pandas as pd
url = 'https://github.com/BiaBalintDevelopers/dcmoderator-roleconfig/blob/main/users.csv'
df = pd.read_csv(url, error_bad_lines=False)
