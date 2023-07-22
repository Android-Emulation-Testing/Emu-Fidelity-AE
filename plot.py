import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import helper
from zipfile import ZipFile


# GLOBAL CONSTANTS 

PATH_TO_FIGURES = "./fig/"
FIGSIZE=(11, 7)
LEGEND_FONTSIZE = 28
LABEL_FONTSIZE = 40
hatches = ['xx', '\\\\', '//', '--', '++', '||', 'o', 'O', '.', '*']
width = 0.35  # the width of the bars
line_width = 3.5
colors = ['#7F449B', '#009D72', '#E5A023']
font = {'family': 'Arial',
        'weight' : 'normal',
        'size'   : 40}
bar_common_args = {"linewidth": line_width, "zorder": 3, "facecolor": "white"}
bar1_args = {"edgecolor": colors[0], "hatch": hatches[0]}
bar2_args = {"edgecolor": colors[1], "hatch": hatches[1]}


# envsetup

plt.rc('font', **font)
plt.rcParams.update({'legend.handlelength': 1.3, 'legend.borderpad': 0.25, "legend.labelspacing": 0.25, "legend.handletextpad": 0.5})
plt.rcParams['hatch.linewidth'] = line_width
pd.set_option("display.max_colwidth", 5000)
pd.set_option("display.max_columns", 10000)
pd.set_option("display.max_rows", 100)
os.makedirs(PATH_TO_FIGURES, exist_ok=True)


# data preparation

# unzip the data
print("Unzipping data.zip...")
with ZipFile("data.zip", 'r') as zObject:
    zObject.extractall(path="./")

print("Reading failure data...")
df = pd.read_csv("data.csv")
df = helper.generate_identifier(df)
freq = helper.get_freq_list(df)

true_positives = freq[(freq["count_phys"] != 0) & (freq["count_virt"] != 0)]["identifier"]
false_positives = freq[(freq["count_phys"] == 0) & (freq["count_virt"] != 0)]["identifier"]
false_negatives = freq[(freq["count_phys"] != 0) & (freq["count_virt"] == 0)]["identifier"]

g_test_rounds = np.array([12, 12, 12, 12, 12, 5, 12, 5, 12, 9]) # the number of test rounds for each app
g_device_version = np.array([172, 243, 373, 692, 1077, 1568, 1438, 355]) # number of devices for each android version

print("Plotting figures...")

# Figure 1: Precision/recall of the test results on virtualized devices, relative to those on physical devices.

# precision: true positives / (true positives + false positives)
# recall: true positives / (true positives + false negatives)

app_id = range(1, 11)

precision = []
recall = []

for id in app_id:
    df_app = df[df["app_id"] == id]
    df_phys_tp = df_app[(df_app["device_model"] != "virt") & (df_app["identifier"].isin(true_positives))]
    df_virt_tp = df_app[(df_app["device_model"] == "virt") & (df_app["identifier"].isin(true_positives))]
    df_fp = df_app[df_app["identifier"].isin(false_positives)]
    df_fn = df_app[df_app["identifier"].isin(false_negatives)]
    precision.append(len(df_virt_tp) / (len(df_virt_tp) + len(df_fp)) * 100)
    recall.append(len(df_phys_tp) / (len(df_phys_tp) + len(df_fn)) * 100)

f, ax = plt.subplots(figsize=FIGSIZE)

x = np.arange(len(app_id))  # the label locations

rects1 = ax.bar(x - width/2 - 0.0, precision, label="Precision", width=width, **bar_common_args, **bar1_args)
rects2 = ax.bar(x + width/2 + 0.0, recall, label="Recall", width=width, **bar_common_args, **bar2_args)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Precision / Recall (%)', size = LABEL_FONTSIZE)
ax.set_xlabel('App ID', size = LABEL_FONTSIZE)
ax.set_xticks(x, app_id)
ax.set_ylim((90, 100))

circ1 = mpatches.Patch(label="Precision", **bar_common_args, **bar1_args)
circ2 = mpatches.Patch(label='Recall', **bar_common_args, **bar2_args)

l2 = ax.legend(handles = [circ1, circ2], loc = 'upper left', bbox_to_anchor=(-0.005, 1.005), fontsize=LEGEND_FONTSIZE, edgecolor = 'black', fancybox = False)
plt.show()

f.savefig(PATH_TO_FIGURES + "fig1_pre_recall_app.pdf", format = "pdf", bbox_inches = 'tight')



# Figure 2: Precision and recall of the test results on virtualized devices for each Android version.

# precision: true positives / (true positives + false positives)
# recall: true positives / (true positives + false negatives)

versions = range(5, 13)

precision = []
recall = []

for v in versions:
    df_v = df[(df["android_version"] >= v) & (df["android_version"] < (v + 1))]
    df_phys_tp = df_v[(df_v["device_model"] != "virt") & (df_v["identifier"].isin(true_positives))]
    df_virt_tp = df_v[(df_v["device_model"] == "virt") & (df_v["identifier"].isin(true_positives))]
    df_fp = df_v[df_v["identifier"].isin(false_positives)]
    df_fn = df_v[df_v["identifier"].isin(false_negatives)]
    precision.append(len(df_virt_tp) / (len(df_virt_tp) + len(df_fp)) * 100)
    recall.append(len(df_phys_tp) / (len(df_phys_tp) + len(df_fn)) * 100)

f, ax = plt.subplots(figsize=FIGSIZE)

x = np.arange(start=5, stop=13)  # the label locations

rects1 = ax.bar(x - width/2 - 0.0, precision, label="Precision", width=width, **bar_common_args, **bar1_args)
rects2 = ax.bar(x + width/2 + 0.0, recall, label="Recall", width=width, **bar_common_args, **bar2_args)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Precision / Recall (%)', size = LABEL_FONTSIZE)
ax.set_xlabel('Android Version', size = LABEL_FONTSIZE)
ax.set_xticks(x, versions)
ax.set_ylim((90, 100))

circ1 = mpatches.Patch(label="Precision", **bar_common_args, **bar1_args)
circ2 = mpatches.Patch(label='Recall', **bar_common_args, **bar2_args)

l2 = ax.legend(handles = [circ1, circ2], loc = 'upper left', bbox_to_anchor=(-0.005, 1.005), fontsize=LEGEND_FONTSIZE, edgecolor = 'black', fancybox = False)

plt.show()

f.savefig(PATH_TO_FIGURES + "fig2_pre_recall_os.pdf", format = "pdf", bbox_inches = 'tight')



# Figure 3: Average failure occurrence frequency per device per test round for different Android versions.

versions = range(5, 13)

freq_phys = []
freq_virt = []

for v in versions:
    df_v = df[(df["android_version"] >= v) & (df["android_version"] < (v + 1))]
    df_phys = df_v[(df_v["device_model"] != "virt")]
    df_virt = df_v[(df_v["device_model"] == "virt")]
    freq_phys.append(len(df_phys) / g_device_version[v-5] / sum(g_test_rounds))
    freq_virt.append(len(df_virt) / g_device_version[v-5] / sum(g_test_rounds))

f, ax = plt.subplots(figsize=(11.7, 7))

x = np.arange(len(versions))  # the label locations
rects1 = ax.bar(x - width/2 - 0.0, freq_phys, label="Physical", width=width, **bar_common_args, **bar1_args)
rects2 = ax.bar(x + width/2 + 0.0, freq_virt, label="Virtualized", width=width, **bar_common_args, **bar2_args)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of Events', fontsize = LABEL_FONTSIZE)
ax.set_xlabel('Android Version', fontsize = LABEL_FONTSIZE)
ax.set_ylim((0.2, 1.0))

ax.set_xticks(x, versions)
circ1 = mpatches.Patch(label="Physical", **bar_common_args, **bar1_args)
circ2 = mpatches.Patch(label='Virtualized', **bar_common_args, **bar2_args)
l2 = ax.legend(handles = [circ1, circ2], loc = 'upper right', bbox_to_anchor=(1.005, 1.005), fontsize=LEGEND_FONTSIZE, edgecolor = 'black', fancybox = False)
# plt.legend(loc="upper right", bbox_to_anchor=(1.005, 1.005), fontsize=LEGEND_FONTSIZE, edgecolor = 'black', fancybox = False)

plt.show()

f.savefig(PATH_TO_FIGURES + "fig3_freq_os.pdf", format = "pdf", bbox_inches = 'tight')



# Figure 4: Average failure occurrence frequency per device per test round for each studied app.

app_id = range(1, 11)

freq_phys = []
freq_virt = []

for id in app_id:
    df_app = df[df["app_id"] == id]
    df_phys = df_app[(df_app["device_model"] != "virt")]
    df_virt = df_app[(df_app["device_model"] == "virt")]
    freq_phys.append(len(df_phys) / sum(g_device_version) / g_test_rounds[id - 1])
    freq_virt.append(len(df_virt) / sum(g_device_version) / g_test_rounds[id - 1])

f, ax = plt.subplots(figsize=FIGSIZE)

x = np.arange(len(app_id))  # the label locations
rects1 = ax.bar(x - width/2 - 0.0, freq_phys, label="Physical", width=width, **bar_common_args, **bar1_args)
rects2 = ax.bar(x + width/2 + 0.0, freq_virt, label="Virtualized", width=width, **bar_common_args, **bar2_args)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of Events', size = LABEL_FONTSIZE)
ax.set_xlabel('App ID', size = LABEL_FONTSIZE)
ax.set_xticks(x, app_id)
ax.set_ylim((0.00, 1.0))

circ1 = mpatches.Patch(label="Physical", **bar_common_args, **bar1_args)
circ2 = mpatches.Patch(label='Virtualized', **bar_common_args, **bar2_args)
l2 = ax.legend(handles = [circ1, circ2], loc = 'upper right', bbox_to_anchor=(1.005, 1.005), fontsize=LEGEND_FONTSIZE, edgecolor = 'black', fancybox = False)
plt.show()

f.savefig(PATH_TO_FIGURES + "fig4_freq_app.pdf", format = "pdf", bbox_inches = 'tight')



# Figure 5: Test precision/recall on our virtualized devices for each app, before and after applying our enhancements.

app_id = range(1, 11)

precision = []
recall = []

for id in app_id:
    df_app = df[df["app_id"] == id]
    df_phys_tp = df_app[(df_app["device_model"] != "virt") & (df_app["identifier"].isin(true_positives))]
    df_virt_tp = df_app[(df_app["device_model"] == "virt") & (df_app["identifier"].isin(true_positives))]
    df_fp = df_app[df_app["identifier"].isin(false_positives)]
    df_fn = df_app[df_app["identifier"].isin(false_negatives)]
    precision.append(len(df_virt_tp) / (len(df_virt_tp) + len(df_fp)) * 100)
    recall.append(len(df_phys_tp) / (len(df_phys_tp) + len(df_fn)) * 100)

# we are still negotiating with the relevant authorities to release our post-enhancement measurement data.
precision_post = [99.03, 99.13, 98.92, 99.29, 99.10, 99.30, 98.99, 99.20, 98.91, 99.45]
recall_post = [94.18, 92.58, 94.14, 94.57, 96.29, 95.31, 94.93, 96.09, 94.49, 95.87]

precision_diff = np.array(precision_post) - np.array(precision)
recall_diff = np.array(recall_post) - np.array(recall)

f, ax = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(app_id))  # the label locations
rects1 = ax.bar(x - width/2 - 0.0, precision, label="Precision", width=width, **bar_common_args, **bar1_args)
rects2 = ax.bar(x + width/2 + 0.0, recall, label="Recall", width=width, **bar_common_args, **bar2_args)
rects1 = ax.bar(x - width/2 - 0.0 , precision_diff, label='Precision', width=width, edgecolor=colors[2], bottom=precision, hatch=hatches[2], **bar_common_args)
rects2 = ax.bar(x + width/2 + 0.0, recall_diff, label='Recall', width=width, edgecolor=colors[2], bottom=recall, hatch=hatches[2], **bar_common_args)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Precision / Recall (%)', size = LABEL_FONTSIZE)
ax.set_xlabel('App ID', size = LABEL_FONTSIZE)
ax.set_xticks(x, app_id)
ax.set_ylim((90, 102.8))
ax.set_yticks([90, 92.5, 95, 97.5, 100], ["90.0", "92.5", "95", "97.5", "100"])

circ1 = mpatches.Patch(label="Original Precision", **bar_common_args, **bar1_args)
circ2 = mpatches.Patch(label='Original Recall', **bar_common_args, **bar2_args)
circ3 = mpatches.Patch(label = 'Enhancement', **bar_common_args, edgecolor=colors[2], hatch=hatches[2])

l2 = ax.legend(handles = [circ1, circ2, circ3], loc = 'upper left', bbox_to_anchor=(-0.005, 1.005), fontsize=LEGEND_FONTSIZE, edgecolor = 'black', fancybox = False, ncol=2)
plt.show()

f.savefig(PATH_TO_FIGURES + "fig5_pre_recall_app_enhanced.pdf", format = "pdf", bbox_inches = 'tight')



# Figure 6: Frequency difference between virtualized and physical devices for each failure type after enhancements.

# frequency differences of common failures. positive values mean virtualized devices fail more frequently
# we are still negotiating with the relevant authorities to release our post-enhancement measurement data.
freq_diff = [-180.64, -162.2060930212022, -144.02318137193345, -138.22658857825803, -133.00941060184687, -127.99751856782662, -116.70809256077162, -108.04714822646554, -103.65401715288341, -99.53766840312653, -92.04486364609521, -88.40648129363747, -85.99209528592242, -77.48732067706194, -74.1559636400636, -71.05691557896449, -67.84565205500917, -65.96170551513876, -63.463561778626016, -60.92281360120168, -56.20248627834037, -53.91829976613923, -51.43419527230087, -48.01862235715774, -46.24472125757876, -43.92820834394455, -41.76356463697887, -40.178258235018845, -38.94729892137153, -36.91963479977932, -35.679378888417276, -34.52057165183527, -33.38013334469669, -31.90713537942283, -30.64573439772649, -29.634389055110592, -28.323733619279455, -27.415680125156758, -26.031526121458242, -25.122189313955964, -24.300020130511754, -23.429905236227327, -22.6013124834397, -21.247909477762462, -20.345191016768368, -19.566465570165803, -18.876249535555715, -18.12524350194517, -17.324109160593558, -16.698576565632713, -15.923720908185263, -15.078400668718054, -14.464985592752882, -13.941847021850666, -13.41724587443267, -12.473461555133667, -11.877480577172651, -11.425401806933952, -10.943212209025223, -10.327615477732905, -9.974662680356943, -9.422319628654446, -9.078008309657758, -8.72098666401141, -8.362159660613408, -8.030447532540567, -7.685183604881992, -7.207936649444431, -6.964085646769121, -6.609516360675258, -6.304907216276682, -6.040748299663214, -5.777538952366058, -5.42404635686966, -5.212921314518379, -4.968143589611923, -4.678340258776398, -4.619560503003722, -4.598643429007261, -4.526498495117977, -4.289084118055033, -4.266272640847902, -4.04165042276381, -4.008344157412761, -3.8487220559117716, -3.7452069592134123, -3.740192426578597, -3.6566570395195193, -3.6550606822143443, -3.648669622504441, -3.574248841361239, -3.466347375753722, -3.4455699494485508, -3.3555113906100793, -3.287072436018711, -3.123328378911623, -3.011071237289027, -3.0044859753560935, -2.903209415758175, -2.8652138651451153, -2.6651968198433735, -2.5525338631550127, -2.5143936183730062, -2.44907577264393, -2.3208704551491586, -2.2534811796257266, -2.2294287715244145, -2.1755431767730258, -2.1464285263331, -2.042682942131634, -1.9663687916412975, -1.8942454754175237, -1.8003266518035268, -1.6577729702197672, -1.6121465511779114, -1.3037816454598143, -1.260563854931334, -1.1786289605476163, -1.1709903222280218, -1.079068315168918, -1.00220448364224, -0.9129239176126678, -0.8126161967046279, -0.6366857794411338, -0.6209229592200316, -0.49346062713283523, -0.45172194354134376, -0.4269104863505717, -0.2662039333653681, -0.25428392675206624, -0.16069535192782602, -0.06994854358238456, -0.06880502714616021, -0.05452367516662804, -0.003684289547301489, 0.003867092107627812, 0.11423492185869222, 0.1373882082641238, 0.17765479633507297, 0.26393371664944176, 0.3958650589793056, 0.4391444197104626, 0.46337695175295757, 0.5356767892985754, 0.5565521486033624, 0.5663872202498403, 0.581603076550083, 0.590770439395218, 0.6225126051919716, 0.6353884615794847, 0.6524227962399731, 0.6785402845281023, 0.6859965080010095, 0.6997180882942757, 0.7534265665184137, 0.7810131518625862, 0.8011134895296053, 0.8117116474254829, 0.8269719862723317, 0.8621215942095652, 0.8772572471085951, 0.9680404071157831, 0.9802237274588403, 1.081541214229361, 1.260718660404553, 1.2965386805224046, 1.4033089166411266, 1.5227348417828006, 1.5844774639280939, 1.5966749351154181, 1.7707936562404782, 1.784040753211201, 1.9435745544717218, 2.078741702436675, 2.134136940792242, 2.192386321658418, 2.2077496156954197, 2.24229266267743, 2.287982706317944, 2.3567633389648623, 2.5788519510492076, 2.7487886180940775, 2.7749260291735354, 2.8169422558111554, 2.8447384710300394, 2.8586151469460956, 2.8795869399173597, 2.9404130600826424, 2.9645168126882364, 2.980672487018019, 3.0973007326382644, 3.101228269105225, 3.2175220930942636, 3.3643970218863695, 3.380147837715783, 4.1813930808665525, 4.182332316827356, 4.3467173985462715, 4.440859013077073, 4.465393178875317, 4.537630735378381, 4.5954875299168965, 4.765757913221529, 4.7718623446344735, 4.78036015752354, 4.882645549079049, 4.90919544089303, 4.978074647123474, 5.155500902019469, 5.157654677011036, 5.175496705816596, 5.188444893521725, 5.393253785536809, 5.4228132089847385, 5.914708393391172, 6.217966642462981, 6.2555206017972065, 6.314675337027667, 6.32172648486682, 6.445355383842167, 6.468808010070806, 6.641547100579155, 7.190754065141339, 7.464773677668113, 7.560874879084139, 7.675106127375864, 8.060363666635435, 8.0625610938428, 8.184617476081383, 8.19967588022563, 8.22898388835213, 8.305105177948576, 8.378134937981356, 8.449362766179883, 8.58379024745031, 8.596898749661296, 8.987274660424033, 9.324100293872409, 9.39592342201421, 9.4084632171387, 9.48596856137001, 9.566325070689022, 9.863265592949347, 9.891927033747976, 10.221377791084588, 10.237506748835639, 10.32584016308651, 10.397331394059387, 10.531287648842062, 10.572375571408912, 10.64970951359148, 10.678542983379428, 11.201504331123306, 11.364867390064575, 11.38780355888938, 11.548889860989235, 11.551571785325669, 11.64251988742862, 11.783328527125295, 11.797110706583005, 11.850474772003032, 11.903725262814895, 11.913695189649157, 12.091072132968186, 12.404161633322168, 12.464233662643736, 13.110142343031987, 13.151480816246622, 13.40527146485622, 13.485463993859728, 13.886503856745772, 13.88689587458736, 14.086939725943196, 14.191215237636227, 14.331584307696613, 14.703752848009604, 14.775409732776671, 14.795384837775586, 14.970955735099505, 15.047734512217618, 15.108982101118466, 15.781165738159334, 16.04496497454442, 16.09758399330166, 16.475689529632213, 16.718618388669064, 16.90709295269164, 17.200042481397595, 17.595244109032596, 17.82375808358419, 17.835242338014904, 17.860965376200436, 17.92033126367321, 17.953948640928655, 18.128447747292835, 18.159105443136774, 18.37719233415081, 18.416526985674068, 18.540125858398664, 19.361417193166044, 19.361709082708803, 19.46789209611273, 19.510909237356326, 19.607518370121383, 19.794291782821198, 19.81306883290093, 20.100045067215305, 20.386372222132692, 20.429296975201066, 20.920786267317908, 21.047955170285242, 21.17156292538445, 21.46317198464383, 21.58253122125207, 21.884703284500212, 22.505112944001176, 22.57762172504057, 22.648814350374096, 22.66313027592402, 22.68130145459946, 22.712470653669264, 22.78462179679071, 24.083818092090485, 24.141333209505248, 24.152633750578417, 24.169878460915566, 24.67665691878951, 25.143784113613115, 25.37023518408184, 26.02170507773274, 26.303062472301434, 27.517237024916266, 27.735336754915753, 28.60690563013908, 29.00960464958298, 29.168182991022533, 29.37454281409542, 30.228112603059312, 31.696189937405176, 31.82868764433331, 32.26987662587911, 32.931960579181975, 33.24466893753733, 34.25032396050254, 34.4785407358496, 36.453609773072415, 41.04084319038341, 41.11730003158819, 41.419915211542005, 42.00804633582274, 45.45687101639493, 48.035976491647176, 48.993020626667885, 50.18922421717838, 50.924960552431926, 51.86739402255456, 54.27998796162824, 57.24533991851213, 58.689731109974645, 62.72606421473668, 74.01582608151497, 77.32622474367656, 86.5721366849176, 95.93828061612477, 100.61870597352176, 109.48182499869512, 109.62697303232565, 111.49600206674846, 129.55682199113573, 151.04557706762347, 182.91273373607174, 183.65673456355873, 203.65304817696006, 207.11]

f, ax = plt.subplots(figsize=(9.6, 7))
plt.ylim((0, 1))
plt.yticks(ticks=[0, 0.2, 0.4, 0.6 ,0.8, 1], labels = ['0', '0.2', '0.4', '0.6' ,'0.8', '1'])
plt.xlim((-250, 250))

# post_per[0] = 201.1
count, bins_count = np.histogram(freq_diff, bins=50)

# finding the PDF of the histogram using count values
pdf = count / sum(count)
  
# using numpy np.cumsum to calculate the CDF
cdf = np.cumsum(pdf)
cdf = np.insert(cdf, 0, 0);

plt.xlabel('Frequency Difference (%)', fontsize = LABEL_FONTSIZE)
plt.ylabel('CDF', fontsize = LABEL_FONTSIZE)
ax.set_xticks([-200, 0, 200], ['-200','0','200'])

# plot the actual lines
plt.plot(bins_count, cdf, color = 'blue', zorder=1, clip_on=False, linewidth=3)
bbox = dict(boxstyle="square,pad=0.3", facecolor='none', edgecolor='black')
def get_bbox_text(freq_diff):
    bbox_text = f"Max = {round(np.max(freq_diff),2)}%\nMean = {round(np.mean(freq_diff),2)}%\nMedian = {round(np.median(freq_diff),2)}%\nMin = {round(np.min(freq_diff),2)}%"
    return bbox_text

plt.annotate(xy=(-210, 0.55), xycoords='data',
                  xytext=(-210, 0.55), textcoords="data", fontsize = LEGEND_FONTSIZE, linespacing=1.5, text=get_bbox_text(freq_diff), bbox=bbox) # arrowprops=dict(arrowstyle = '-|>', relpos = (0,1), shrinkA = 0, color = 'black'))

f.savefig(PATH_TO_FIGURES + "fig6_freq_discrepancy_cdf.pdf", format = "pdf", bbox_inches = 'tight')



# Table 2: The 27 phone vendors and their corresponding numbers of device models (# Models) involved in our study.

precisions = []
recalls = []

brands = ["samsung", "xiaomi", "huawei", "vivo", "oppo", "honor", "redmi", "meizu", "lg", "docomo", "motorola", "infinix", "realme", "tecno", "google", "lenovo", "sony", "oneplus", "smartisan", "vsmart", "asus", "zte", "alcatel", "blackshark", "nubia", "alldocube", "blackview"]
device_count = np.array([1863, 959, 901, 540, 291, 198, 193, 179, 119, 84, 82, 77, 66, 61, 54, 44, 39, 38, 29, 28, 17, 17, 14, 11, 6, 5, 3]) # number of devices for each brand, sorted by failure count
regions = ["US", "China", "China", "China", "China", "China", "China", "China", "Korea", "Japan", "US", "US", "China", "S. Africa", "US", "China", "Europe", "India", "China", "Vietnam", "Europe", "China", "US", "China", "China", "China", "US"]
cts = ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"]

for brand in brands:
    df_brand = df[df["device_brand"] == brand]
    df_phys_tp = df_brand[(df_brand["device_model"] != "virt") & (df_brand["identifier"].isin(true_positives))]
    df_virt_tp = df_brand[(df_brand["device_model"] == "virt") & (df_brand["identifier"].isin(true_positives))]
    df_fp = df_brand[df_brand["identifier"].isin(false_positives)]
    df_fn = df_brand[df_brand["identifier"].isin(false_negatives)]
    precisions.append(len(df_virt_tp) / (len(df_virt_tp) + len(df_fp)) * 100)
    recalls.append(len(df_phys_tp) / (len(df_phys_tp) + len(df_fn)) * 100)

# prettier precision and recall
precisions = [str(round(x, 1)) + "%" for x in precisions]
recalls = [str(round(x, 1)) + "%" for x in recalls]

print("Table 2: The 27 phone vendors and their corresponding numbers of device models (# Models) involved in our study. The rightmost four columns respectively denote the country/region in which the vendor obtains the most sales revenue (Region), whether the device models are CTS/VTS-compliant (C/VTS), the Precision and Recall of the test results on virtualized devices for each vendor.")
print()
print(pd.DataFrame({"Vendor": brands, "# Models": device_count, "Region": regions, "C/VTS": cts, "Precision": precisions, "Recall": recalls}))
print()



# Table 3: The top-10 most frequent types of failures. 

entities = ["App", "Third-party", "App", "App", "App", "App", "App", "App", "App", "App"]

total_freq = freq.copy()
total_freq["count"] = total_freq["count_phys"] + total_freq["count_virt"]
total_freq["portion"] = total_freq["count"] / freq[freq["identifier"].isin(true_positives)]["count"].sum()
total_freq = total_freq.sort_values(by="count", ascending=False).reset_index(drop=True)[:10]

portions = (total_freq["portion"] * 100).round(1).astype(str) + "%"
reasons = [x["identifier"] for idx, x in total_freq.iterrows()]
apps = [sorted(df[df["identifier"] == x["identifier"]]["app_id"].unique()) for idx, x in total_freq.iterrows()]

print("Table 3: The top-10 most frequent types of failures. The columns respectively denote the ranking of the failure type in terms of frequency (No.), the portion of failure events (Portion), the IDs of the apps under influence (App-ID), the responsible Entity for the failure (i.e., an app, a vendor, the OS, the emulator, or a third-party component), the triggered Exception/Signal of the failure, and the Root Cause of each failure.")
print()
print(pd.DataFrame({"No.": range(1, 11), "Portion": portions, "App-ID": apps, "Entity": entities, "Root Cause": reasons}))
print()



# Table 4: The top-5 most frequent types of false negative failures. The columns denote the same meanings as in Table 3.

entities = ["AOSP", "Meizu", "MediaTek", "Samsung", "OPPO"]

fn_freq = freq[freq["identifier"].isin(false_negatives)].copy()
fn_freq["count"] = fn_freq["count_phys"] + fn_freq["count_virt"]
fn_freq["portion"] = fn_freq["count"] / freq[freq["identifier"].isin(false_negatives)]["count"].sum()
fn_freq = fn_freq.sort_values(by="count", ascending=False).reset_index(drop=True)[:5]

portions = (fn_freq["portion"] * 100).round(1).astype(str) + "%"
reasons = [x["identifier"] for idx, x in fn_freq.iterrows()]
apps = [sorted(df[df["identifier"] == x["identifier"]]["app_id"].unique()) for idx, x in fn_freq.iterrows()]

print("Table 4: The top-5 most frequent types of false negative failures. The columns denote the same meanings as in Table 3.")
print()
print(pd.DataFrame({"No.": range(1, 6), "Portion": portions, "App-ID": apps, "Entity": entities, "Root Cause": reasons}))
print()



# Table 5: The top-5 most frequent types of false positive failures. The columns denote the same meanings as in Table 3.

entities = ["AOSP, Emulator", "Emulator", "AOSP, Emulator", "Third-party", "Emulator"]

fp_freq = freq[freq["identifier"].isin(false_positives)].copy()
fp_freq["count"] = fp_freq["count_phys"] + fp_freq["count_virt"]
fp_freq["portion"] = fp_freq["count"] / freq[freq["identifier"].isin(false_positives)]["count"].sum()
fp_freq = fp_freq.sort_values(by="count", ascending=False).reset_index(drop=True)[:5]

portions = (fp_freq["portion"] * 100).round(1).astype(str) + "%"
reasons = [x["identifier"] for idx, x in fp_freq.iterrows()]
apps = [sorted(df[df["identifier"] == x["identifier"]]["app_id"].unique()) for idx, x in fp_freq.iterrows()]

print("Table 5: The top-5 most frequent types of false positive failures. The columns denote the same meanings as in Table 3.")
print()
print(pd.DataFrame({"No.": range(1, 6), "Portion": portions, "App-ID": apps, "Entity": entities, "Root Cause": reasons}))
print()
