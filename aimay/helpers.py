# return reply message(from data/*.txt)
def return_data(filename):
    filepath = os.getcwd() + '/data/' + filename
    with open(filepath) as datafile:
        datalines = datafile.readlines()
    return datalines[random.randint(0,(len(datalines) - 1))].strip()


