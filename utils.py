
def autolabel(plt, rects, count_list=None):
    # attach a text label above each bar in rects, displaying its height
    assert len(rects) == len(count_list)
    if count_list != None:
        for rect, count in zip(rects, count_list):
            # height = rect.get_height()
            plt.annotate(
                '{}'.format(count),
                xy=(rect.get_x() + rect.get_width() / 2, 100),
                # xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom'
            )
    else:
        for rect in rects:
            height = rect.get_height()
            plt.annotate(
                '{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, 100),
                # xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom'
            )        
