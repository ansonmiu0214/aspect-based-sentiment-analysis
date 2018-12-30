import matplotlib.pyplot as plt


#Use this function to display results from training to see the number of true and false postivies and false negatives from extractino
def plot_piechart(metric_values, option, name):
    total = sum(metric_values)
    sizes = list(map(lambda x: x / total * 100, metric_values))
    print(sizes)
    labels = ['True Positives', 'False Positives', 'False Negatives']
    fig1,ax1 = plt.subplots()
    if option == 'E':
        fig1.suptitle("Entity -  %s" % (name), va='top')
    else:
        fig1.suptitle("Attributes of %s" % (name), va='top')


    ax1.pie(sizes, labels=labels, startangle=90,autopct='%1.1f%%')
    ax1.axis('equal')
    plt.show()

#This function can be used to see bias from different sources. Points far from the average line suggest bias
def plot_linegraph(aspect_sent_pairs,aspect_name):
    x = [x for x in range(1, len(aspect_sent_pairs) + 1)]
    y = []
    labels = []

    for p in aspect_sent_pairs:
        labels.append(p[0])
        y.append(p[1])

    avg = sum(y) / len(y)

    plt.plot(x,[avg for k in range(len(y))],'--')
    plt.title("Sentiment scores for %s" % (aspect_name))

    plt.plot(x,y,'ro')
    plt.xticks(x,labels,rotation='horizontal')
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.1)
    plt.show()

if __name__ == '__main__':
    #plot_piechart([10,10,10],'A','Apple')
    pairs = [('A',1),('B',2), ('C',3),('D',4),('E',5)]
    plot_linegraph(pairs,'Apples stocks')

