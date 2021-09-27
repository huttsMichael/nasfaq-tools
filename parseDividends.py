import optimalDividends
import matplotlib
import matplotlib.pyplot

if __name__ == '__main__':
    divs = optimalDividends.Dividends()
    fig, ax = matplotlib.pyplot.subplots()
    matplotlib.pyplot.grid(color="#29282c")
    fig.patch.set_facecolor('#2e2d31')
    ax.patch.set_facecolor('#2e2d31')

    dateLen = len(divs.histDates)
    print(divs.histDates)
    for holo in divs.currentMembers:
        print(holo)
        priceLen = len(divs.currentMembers[holo]) 
        lenDif = dateLen - priceLen
        ax.plot(divs.histDates[lenDif:], divs.currentMembers[holo], label=holo)
    
    date_fmt = '%m/%d/%y'
    date_formatter = matplotlib.dates.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())
    matplotlib.pyplot.gca()
    matplotlib.pyplot.legend(prop={'size':8})
    fig.autofmt_xdate()
    matplotlib.pyplot.show()
