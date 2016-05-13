import pandas as pd
import numpy as np

MISSING = ''

def convert_to_datetime(df, cols):
	'''
	INPUT: Pandas DataFrame, List of Columns
	OUTPUT: Pandas DataFrame

	Converts each column in cols to datetime
	'''
	for col in cols:
		df[col] = pd.to_datetime(df[col])
	return df

def extract_col(df, cols, new_cols, symbol):
	'''
	INPUT: Pandas DataFrame, List of Original Columns, List of New Columns, Char
	OUTPUT: Pandas DataFrame

	Loops through zip(cols, new_cols) and extracts information before
	the requested symbol
	'''
	for col1, col2, in zip(cols, new_cols):
		df[col2] = map(lambda x: x.split(symbol)[0], df[col1])
	return df

def remove_word(df, cols, word):
	'''
	INPUT: Pandas DataFrame, List of Columns, Str
	OUTPUT: Pandas DataFrame

	Removes word from each column in cols. Returns DataFrame
	'''
	for col in cols:
		df[col] = map(lambda x: x.replace(word, '').strip() if isinstance(x, str) else x, df[col])
	return df

def parse_ht(ht):
	'''
	INPUT: Row from Pandas DataFrame (type unknown)
	OUTPUT: Float

	Converts feet and inches from string to float. Returns blank
	string otherwise
	'''
	ht_ = ht.split("' ")
	if ht_ in [[''], ['none or unspecified']]:
		return ''
	ft_ = float(ht_[0].strip('"'))
	in_ = float(ht_[1].strip('"'))
	return (12*ft_) + in_

def convert_to_inches(df, cols):
	'''
	INPUT: Pandas DataFrame, List of Columns
	OUTPUT: Pandas DataFrame

	Converts each column in cols to inches.
	'''

	for col in cols:
		df[col] = df[col].apply(parse_ht)

	return df

def convert_to_lower(df, cols):
	'''
	INPUT: Pandas DataFrame, List of Columns
	OUTPUT: Pandas DataFrame

	Converts each column in cols to lowercase
	'''

	for col in cols:
		df[col] = df[col].replace({np.nan: MISSING})
		df[col] = df[col].apply(str.lower)
	return df

def namestr(obj, namespace):
	'''
	INPUT: Object and a namespace
	OUTPUT: List of names that match objects
	'''
	return [name for name in namespace if namespace[name] is obj]

if __name__ == '__main__':


	train_df = pd.read_csv('../data/Train.csv', header=0, low_memory=False)
	test_df = pd.read_csv('../data/test.csv', header=0, low_memory=False)

	str_train = train_df.columns[10:]
	str_test = test_df.columns[9:]

	for model, str_col in zip([train_df, test_df], [str_train, str_test]):

		model = convert_to_datetime(model, ['saledate'])


		model = convert_to_lower(model, str_col)
		model = convert_to_inches(model, ['Stick_Length'])

		remove_inch = ['Undercarriage_Pad_Width', 'Tire_Size']
		remove_w = ['Enclosure']
		remove_quote = ['Blade_Width']

		model = remove_word(model, remove_inch, 'inch')
		model = remove_word(model, remove_w, 'w ')
		model = remove_word(model, remove_quote, "'")

		before_dash = ['fiProductClassDesc']
		new_before_dash = ['fiProductClassDesc_class']
		model = extract_col(model, before_dash, new_before_dash, '-')
		
		model.to_csv('../data/{}_clean.csv'.format(namestr(model, globals())[0][:-3]), delimiter=',')

