from graphfunction import LineGraph,BarChart

'''The makeBarChart function creates a plotly bar chart fig object
    and saves the fig object as an image (.png file)'''
def makeBarChart():
    openGraph = BarChart('open')\
        .convertDatetimeToDate()\
        .groupByDay()\
        .convertSecondsToMinutes()
    fig = openGraph.makeBarChart()
    openGraph.saveImage(fig)

'''The makeLineGraph function creates a plotly line graph fig object
    and saves the fig object as an image (.png file)'''
def makeLineGraph():
    lineGraph = LineGraph('temp').addOpenIndicator().splitData()
    fig = lineGraph.makeLineGraph()
    lineGraph.saveImage(fig)

def main():
    makeBarChart()
    makeLineGraph()

if __name__ == '__main__':
    main()
