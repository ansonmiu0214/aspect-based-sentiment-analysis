import matplotlib.pyplot as plt

def plot_piechart(metric_values):
    total = sum(metric_values)
    sizes = list(map(lambda x: x / total * 100, metric_values))
    print(sizes)
    labels = ['True Positives', 'False Positives', 'False Negatives']
    fig1,ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, startangle=90,autopct='%1.1f%%')
    ax1.axis('equal')
    plt.show()

def plot_linegraph(aspect_sent_pairs):

    x = [x for x in range(1, len(aspect_sent_pairs) + 1)]
    y = []
    labels = []

    for p in aspect_sent_pairs:
        labels.append(p[0])
        y.append(p[1])

    avg = sum(y) / len(y)

    plt.plot(x,[avg for k in range(len(y))],'--')

    plt.plot(x,y,'ro')
    plt.xticks(x,labels,rotation='vertical')
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.1)
    plt.show()

if __name__ == '__main__':
    #plot_piechart([10,10,10])
    pairs = [('A',1),('B',2), ('C',3),('D',4),('E',5)]
    plot_linegraph(pairs)

