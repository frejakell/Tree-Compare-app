import rf_dist, Hist_plot,Center_Trees,KC_dist,T_dist,Q_dist,T_dist_list,Q_dist_list,H_Map,tree_run, rf_colour, KC_tree, PC_dist, Quar_colour
import scipy
import PIL
import math
import sys
import subprocess
from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from io import StringIO
import base64
from random import sample
from django.shortcuts import render, redirect
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from crud.models import Metric, Matrix, Tree_model
import io,os
import pylab
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster import hierarchy as hier
from scipy.spatial import distance as ssd
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import cut_tree
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import ward, dendrogram,complete,average
import random
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, CircleFace


def index(request):
   
    return render(request, 'crud/index.html')

def Results_Display(request):
    context = {}
    if request.method == 'POST':
        metric= request.POST.get('myselect')      
        test=Matrix.objects.get(name=metric.replace(" ", "") )
        gt=np.frombuffer(test.pieces, dtype=np.float64)
       
        list_m=Metric.objects.get(name="Metrics")
        list_m.selected= metric.replace(" ", "")
        list_m.save()
        
        ai=int(math.sqrt(len(gt)))
        shape = ( ai, ai)
        #print(ai)
        Tree_array=[]
        for i in range (ai):
            Tree_array.append("Tree"+str(i+1))
        gt.shape=shape 
        table_metric=gt 
        
        context["Tree_list"]=Tree_array
        context["table_select"]=table_metric
        context["selected"]=metric
        context["Centers"]=Center_Trees.main(table_metric,"n")
        metrics_list= list_m.textfield
        metrics_list=metrics_list.replace('[', '')
        metrics_list=metrics_list.replace(']', '')
        metrics_list=metrics_list.replace("'", '')
        metrics_list=metrics_list.split(",")
        print("------------------------------------------------------------------------------------------------------")
        print(metrics_list)
        context["list_m"]= metrics_list
       
    return render(request, 'crud/Results_D.html',context)

def Results(request):
    if request.method == 'POST':
        flag = request.POST.get('flag')
        m_text1 = request.POST.get('metrics_text_unrooted')
        m_text2 = request.POST.get('metrics_text_rooted')
        #table_metrics = request.POST.get('myTableData')
        m_text=m_text1+m_text2
     
        metric_array=m_text.split(";")
        myset = set(metric_array)
        metric_array= list(myset)
        print(metric_array)
        input=""
        ls=[]
        DRF=[]
        DT=[]
        DKC=[]
        KCList=[]
        context = {}
        for i in metric_array: 
            kc_m=i.replace(' ', '')
            if  kc_m.startswith('Kendall-Colijn'):
                KCList.append(kc_m[14:])  
      
        print(KCList)
        DQ=[]
        if flag=="False" :
            # getting values from post
            input = request.POST.get('input')
            input=input.replace('\n', ' ').replace('\r', '')
            
            Metric.objects.all().delete()
            Matrix.objects.all().delete()
            Tree_model.objects.all().delete()
            newmodel = Metric()
            newmodel.textfield = input
            newmodel.name = "newicks"
            newmodel.save()
            Trees = Tree_model()
            Trees.Tree1 = 1
            Trees.Tree1 = 2
            Trees.name = "trees_det"
            Trees.top="" 
            Trees.save()
            test=Metric.objects.get(name="newicks")
            print(test.textfield)
            ls=[]
            Tree_array = [] 
            list_input=input.split(';')    
            for i in range (len(list_input)):
                Tree_array.append("Tree"+str(i))
            if("Robinson-Fould" in metric_array):
                ls.append("RobinsonFould") 
          
                array = [] 
                list_input=input.split(';')    
                for line in list_input:
                    array.append(line+';')
                array = array[:-1]
                DRF = scipy.zeros([len(array),len(array)])
                names=[]
                w=len(array)
                for i in range(0,w):
                   for j in range(i):
                        #print(array)
                        #print("------------------------------------------------------------------------------------------")
                        DRF[i,j] =DRF[j,i]= rf_dist.main(array[i], array[j])
                #print(DRF[0])
                newboard = Matrix()
                newboard.pieces=DRF
                newboard.name = "RobinsonFould"
                newboard.save()
                #context["tableRF"]=DRF
                
                #context["Centers_RobinsonFould"]=Center_Trees.main(DRF,"y")
                
            if("Triplets" in metric_array):
                ls.append("Triplets") 
          
                array = [] 
                list_input=input.split(';')    
                for line in list_input:
                    array.append(line+';')
                array = array[:-1]
                DT = scipy.zeros([len(array),len(array)])
                w=len(array)
                for i in range(0,w):
                   for j in range(i):
                        #print(array)
                        #print("------------------------------------------------------------------------------------------")
                        DT[i,j] =DT[j,i]= T_dist.main(array[i], array[j])
                newboard = Matrix()
                newboard.pieces=DT
                newboard.name = "Triplets"
                newboard.save() 
                #context["tableT"]=DT
                #context["Centers_Triplets"]=Center_Trees.main(DT,"y")
            if("Quartets" in metric_array):
                ls.append("Quartets") 
          
                array = [] 
                list_input=input.split(';')    
                for line in list_input:
                    array.append(line+';')
                array = array[:-1]
                DQ = scipy.zeros([len(array),len(array)])
                w=len(array)
                for i in range(0,w):
                   for j in range(i):
                        #print(array)
                        #print("------------------------------------------------------------------------------------------")
                        DQ[i,j] =DQ[j,i]= Q_dist.main(array[i], array[j])
                newboard = Matrix()
                newboard.pieces=DQ
                newboard.name = "Quartets"
                newboard.save()
                #context["tableQ"]=DQ
                #context["Centers_Quartets"]=Center_Trees.main(DQ,"y")
            if(len(KCList)>0):
                for h in KCList:
                    ls.append("Kendall-Colijn"+str(h)) 
                   
                    array = [] 
                    list_input=input.split(';')    
                    for line in list_input:
                        array.append(line+';')
                    array = array[:-1]
                    DKC = scipy.zeros([len(array),len(array)])
                    names=[]
                    w=len(array)
                    for i in range(0,w):
                        for j in range(i):
                        #print(array)
                        #print("------------------------------------------------------------------------------------------")
                            DKC[i,j] =DKC[j,i]= KC_dist.main(array[i], array[j], float(h))
                    print(h)
                    print(DKC)
                    newboard = Matrix()
                    newboard.pieces=DKC
                    newboard.name = "Kendall-Colijn"+str(h)
                    newboard.save()
                    #context["tableKC"+str(h)]=DKC
                    #context["Centers_Kendall-Colijn"+str(h)]=Center_Trees.main(DKC,"y")

        Listmodel = Metric()
        Listmodel.textfield = ls
        Listmodel.name = "Metrics"
        Listmodel.save()
        Listmodel = Metric()
        Listmodel.textfield = ls
        Listmodel.name = "Metric1"
        Listmodel.save()
        Listmodel = Metric()
        Listmodel.textfield = ls
        Listmodel.name = "Metric2"
        Listmodel.save()
        Listmodel = Metric()
        Listmodel.textfield = ls
        Listmodel.name = "Metric3"
        Listmodel.save()
        Listmodel = Metric()
        Listmodel.textfield = ls
        Listmodel.name = "Metric4"
        Listmodel.save()
       
        context["table_select"]=[]
        context["selected"]="metric"
        context["Centers"]=""
        context["list_m"]=ls
        context["Tree_list"]=Tree_array
       
        return render(request, 'crud/Results.html',context)
        
def Tree_View(request):
    
    t1 = request.POST.get('Tree1')

    if t1 is None:
        t1=1
    t2 = request.POST.get('Tree2')
    if t2 is None:
        t2=1
    mt = request.POST.get('metric')
    mt=mt.replace(' ','')
    top = request.POST.get('leftsideMenu')
    print(top)
    test=Metric.objects.get(name="newicks")
    Trees=Tree_model.objects.get(name="trees_det")
    Trees.Tree1=t1
    Trees.Tree2=t2
    Trees.Metric=mt
    if(top):
        Trees.top=top
    Trees.save()
    input=test.textfield
    list_input=input.split(';')
    array = []         
    for line in list_input:
        array.append(line+';')
    array = array[:-1]
 
    newick_input1=array[int(t1)-1]
    newick_input2=array[int(t2)-1]
    '''
    process = subprocess.Popen(['python','tree_run.py', test_input ], stdout=subprocess.PIPE)
    output = process.stdout.read()
    
    #jpgfile = Image.open("crud/static/crud/Tree1.png")

    #print( jpgfile.format)
    
    exitstatus = process.poll()
    file = open('crud/static/crud/Tree1.png', "rb").read()
    rea_response = HttpResponse(file, content_type='image/png')
    rea_response['Content-Disposition'] = 'attachment; filename={}'.format('name.png')
    #return rea_response'''
    options=[]
   
    if(mt=="Quartets"): 
        options=Q_dist_list.main(newick_input1,newick_input2)
    elif(mt=="Triplets"):
        options=T_dist_list.main(newick_input1,newick_input2)
    elif(mt[0]=="K"):
        options=["Topology", "Branch Length"]
    context={}
    input_model=Metric.objects.get(name="newicks")
    test=input_model.textfield
    test=test.replace("'", '')
    test=test.split(";")
    context["List_trees"]=test
    list_m=Metric.objects.get(name="Metrics")
    list_tree_num=range(1, len(test))
    metrics_list= list_m.textfield
    metrics_list=metrics_list.replace('[', '')
    metrics_list=metrics_list.replace(']', '')
    metrics_list=metrics_list.replace("'", '')
    metrics_list=metrics_list.split(",")

    context["options"]= options
    context["list_m"]= metrics_list
    context["selected"]=mt
    context["num_list"]= list_tree_num
    context["new1"]= newick_input1
    context["new2"]= newick_input2
    context["tree1"]=t1
    context["tree2"]= t2
    print(test)
    return render(request, 'crud/TreeView.html',context)
    
def testcall(request):
   print("did it work?----------------------------------------")
   process = subprocess.Popen(['python','tree_run2.py'], stdout=subprocess.PIPE)
   output = process.stdout.read()
   exitstatus = process.poll()
   return HttpResponse("it did!")
   
   
def Tree1(request, t1):
    
    #t1= request.POST.get('tree1')
    Trees=Tree_model.objects.get(name="trees_det")
    
    
    #mt = request.POST.get('metric')
    test=Metric.objects.get(name="newicks")
    if(int(t1)==1):
        tree_ind=Trees.Tree1
        tree_ind2=Trees.Tree2
    else:
        tree_ind=Trees.Tree2
        tree_ind2=Trees.Tree1
    input=test.textfield
    list_input=input.split(';')
    array = []         
    for line in list_input:
        array.append(line+';')
    array = array[:-1]
    print(array[tree_ind-1])
    top=Trees.top
    test_input=array[int(tree_ind)-1]
    test_input2=array[int(tree_ind2)-1]
  
    if(Trees.Metric=="RobinsonFould"):
        
        process = subprocess.Popen(['python','rf_colour.py', test_input,test_input2, t1 ], stdout=subprocess.PIPE)
        output = process.stdout.read()
       
        #jpgfile = Image.open("crud/static/crud/Tree1.png")

        #print( jpgfile.format)
        
        exitstatus = process.poll()
    elif(Trees.Metric[0]=="K"):
        process = subprocess.Popen(['python','KC_tree.py', test_input, t1 ], stdout=subprocess.PIPE)
        output = process.stdout.read()
    elif(Trees.Metric[0]=="Q" or Trees.Metric[0]=="T"):
        if(Trees.top):
            leafs=Trees.top

            process = subprocess.Popen(['python','Quar_colour.py', test_input,leafs, t1 ], stdout=subprocess.PIPE)
            output = process.stdout.read()
    
    
    
    else:
        process = subprocess.Popen(['python','tree_run.py', test_input, t1 ], stdout=subprocess.PIPE)
        output = process.stdout.read()
       
        #jpgfile = Image.open("crud/static/crud/Tree1.png")

        #print( jpgfile.format)
        
        exitstatus = process.poll()
    if(int(t1)==1):
        file = open('crud/static/crud/Tree1.png', "rb").read()
    else:
        file = open('crud/static/crud/Tree2.png', "rb").read()
    rea_response = HttpResponse(file, content_type='image/png')
    rea_response['Content-Disposition'] = 'attachment; filename={}'.format('name.png')
    return rea_response
    #return HttpResponse('what you want to output to web')
 
    #return HttpResponse('what yo
def split2(request):
       
        
    if request.method == 'POST':
        context = {}
        metric1= request.POST.get('myselect1')
        list_m=Metric.objects.get(name="Metrics")  
        if(metric1 != '-1' and metric1 != ''):      
            test=Matrix.objects.get(name=metric1.replace(" ", "") )
            gt=np.frombuffer(test.pieces, dtype=np.float64)
           
            
            #print(gt)
            ai=int(math.sqrt(len(gt)))
            shape = ( ai, ai)
            #print(ai)
            gt.shape=shape 
            table_metric1=gt      
            context["table_select1"]=table_metric1
            context["selected1"]=metric1
            context["Centers1"]=Center_Trees.main(table_metric1,"y")
          
        metric2= request.POST.get('myselect2')     
        if(metric2 != '-1' and metric2 != ''):      
            test=Matrix.objects.get(name=metric2.replace(" ", "") )
            gt=np.frombuffer(test.pieces, dtype=np.float64)
           
            
            #print(gt)
            ai=int(math.sqrt(len(gt)))
            shape = ( ai, ai)
            #print(ai)
            gt.shape=shape 
            table_metric2=gt      
            context["table_select2"]=table_metric2
            context["selected2"]=metric2
            context["Centers2"]=Center_Trees.main(table_metric2,"y")
        metrics_list= list_m.textfield
        metrics_list=metrics_list.replace('[', '')
        metrics_list=metrics_list.replace(']', '')
        metrics_list=metrics_list.replace("'", '')
        metrics_list=metrics_list.split(",")
        print("------------------------------------------------------------------------------------------------------")
        print(metrics_list)
        context["list_m"]= metrics_list
       
        print("------------------------------------------------------------------------------------------------------")
        print(metrics_list)
        context["list_m"]= metrics_list
        return render(request, 'crud/Thrid_again.html', context)    
def Results_split(request):
    if request.method == 'POST':
        list_m=Metric.objects.get(name="Metrics")
        split_type= request.POST.get('split_type')
        context = {}
        
        if( split_type=="False"):
            metric1= request.POST.get('myselect1')
            list_m=Metric.objects.get(name="Metrics")  
            print("Metric:-----------------------------------    ",metric1)
            if(metric1 != '-1' and metric1 != ''):      
                test=Matrix.objects.get(name=metric1.replace(" ", "") )
                gt=np.frombuffer(test.pieces, dtype=np.float64)
               
                list_m=Metric.objects.get(name="Metric1")
                list_m.selected= metric1.replace(" ", "")
                list_m.save()
                #print(gt)
                ai=int(math.sqrt(len(gt)))
                shape = ( ai, ai)
                #print(ai)
                gt.shape=shape 
                table_metric1=gt      
                context["table_select1"]=table_metric1
                context["selected1"]=metric1
                context["Centers1"]=Center_Trees.main(table_metric1,"y")
              
            metric2= request.POST.get('myselect2')     
            if(metric2 != '-1' and metric2 != ''):      
                test=Matrix.objects.get(name=metric2.replace(" ", "") )
                gt=np.frombuffer(test.pieces, dtype=np.float64)
                list_m=Metric.objects.get(name="Metric2")
                list_m.selected= metric2.replace(" ", "")
                list_m.save()
                
                #print(gt)
                ai=int(math.sqrt(len(gt)))
                shape = ( ai, ai)
                #print(ai)
                gt.shape=shape 
                table_metric2=gt      
                context["table_select2"]=table_metric2
                context["selected2"]=metric2
                context["Centers2"]=Center_Trees.main(table_metric2,"y")
            metric3= request.POST.get('myselect3')
     
            if(metric3 != '-1' and metric3 != ''):      
                test=Matrix.objects.get(name=metric3.replace(" ", "") )
                gt=np.frombuffer(test.pieces, dtype=np.float64)
                list_m=Metric.objects.get(name="Metric3")
                list_m.selected= metric3.replace(" ", "")
                list_m.save()
                
                #print(gt)
                ai=int(math.sqrt(len(gt)))
                shape = ( ai, ai)
                #print(ai)
                gt.shape=shape 
                table_metric3=gt      
                context["table_select3"]=table_metric3
                context["selected3"]=metric3
                context["Centers3"]=Center_Trees.main(table_metric3,"y")
              
            metric4= request.POST.get('myselect4')     
            if(metric4 != '-1' and metric4 != ''):      
                test=Matrix.objects.get(name=metric4.replace(" ", "") )
                gt=np.frombuffer(test.pieces, dtype=np.float64)
               
                list_m=Metric.objects.get(name="Metric4")
                list_m.selected= metric4.replace(" ", "")
                list_m.save()
                #print(gt)
                ai=int(math.sqrt(len(gt)))
                shape = ( ai, ai)
                #print(ai)
                gt.shape=shape 
                table_metric4=gt      
                context["table_select4"]=table_metric4
                context["selected4"]=metric4
                context["Centers4"]=Center_Trees.main(table_metric4,"y")
            Tree_array=[]
            for i in range (ai):
                Tree_array.append("Tree"+str(i+1))
            context["Tree_list"]=Tree_array
            metrics_list= list_m.textfield
            metrics_list=metrics_list.replace('[', '')
            metrics_list=metrics_list.replace(']', '')
            metrics_list=metrics_list.replace("'", '')
            metrics_list=metrics_list.split(",")
           
            context["list_m"]= metrics_list

            return render(request, 'crud/Thrid_again.html', context)    
        else:   
       
            context={}
            metrics_list= list_m.textfield
            metrics_list=metrics_list.replace('[', '')
            metrics_list=metrics_list.replace(']', '')
            metrics_list=metrics_list.replace("'", '')
            metrics_list=metrics_list.split(",")
           
            context["list_m"]= metrics_list
        return render(request, 'crud/Thrid_again.html', context)

def HeatMap(request,t1):
    # Creamos los datos para representar en el gráfico
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from scipy.cluster.hierarchy import ward, dendrogram,complete
    from scipy.cluster import hierarchy as hier
    from scipy.spatial import distance as ssd
    import scipy.cluster.hierarchy as sch
    t1=int(t1)
    if(t1==0):
        list_m=Metric.objects.get(name="Metrics")
    elif(t1==1): 
        list_m=Metric.objects.get(name="Metric1")
    elif(t1==2):
        list_m=Metric.objects.get(name="Metric2")
    elif(t1==3): 
        list_m=Metric.objects.get(name="Metric3")
    else:
        list_m=Metric.objects.get(name="Metric4")
   
    test=Matrix.objects.get(name=list_m.selected)
    
    gt=np.frombuffer(test.pieces, dtype=np.float64)
    
    ai=int(math.sqrt(len(gt)))
    shape = ( ai, ai)
    print(ai)
   
    gt.shape=shape
    print("gt is: ",gt)
    distArray = ssd.squareform(gt)
    print("matrix is: ", distArray)
    fig = Figure()
    ax1 = fig.add_axes([0.05,0.3,0.2,0.6])
    Y = ward(distArray)
    Z1 = sch.dendrogram(Y, orientation='left')
    ax1.set_xticks([])
    ax1.set_yticks([])
    axmatrix = fig.add_axes([0.3,0.3,0.6,0.6])
    idx1 = Z1['leaves']
   
    D = gt[idx1,:]
    D = D[:,idx1]
    im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu,vmin=0, vmax=8)
 
    axcolor = fig.add_axes([0.91,0.3,0.02,0.6])
    fig.colorbar(im, cax=axcolor)
   
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    
    canvas.print_png(response)
    fig.clear()
    return response
def Hist(request, t1):
  # Creamos los datos para representar en el gráfico
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    t1=int(t1)
    if(t1==0):
        list_m=Metric.objects.get(name="Metrics")
    elif(t1==1): 
        list_m=Metric.objects.get(name="Metric1")
    elif(t1==2):
        list_m=Metric.objects.get(name="Metric2")
    elif(t1==3): 
        list_m=Metric.objects.get(name="Metric3")
    else:
        list_m=Metric.objects.get(name="Metric2")
   
   
    test=Matrix.objects.get(name=list_m.selected)
    gt=np.frombuffer(test.pieces, dtype=np.float64)
    print(gt)
    #ai=int(math.sqrt(len(gt)))
    #shape = ( ai, ai)
    #print(ai)
    #gt.shape=shape 
    #print(gt)
    fig=Figure()
    ax=fig.add_subplot(111)
    #ax.plot(range(10), range(10),color='red',linestyle='dashed', marker='3')
    ax.hist(gt,bins=20)
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
def MDS_text(request, t1):
  # Creamos los datos para representar en el gráfico
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    t1=int(t1)
    if(t1==0):
        list_m=Metric.objects.get(name="Metrics")
    elif(t1==1): 
        list_m=Metric.objects.get(name="Metric1")
    elif(t1==2):
        list_m=Metric.objects.get(name="Metric2")
    elif(t1==3): 
        list_m=Metric.objects.get(name="Metric3")
    else:
        list_m=Metric.objects.get(name="Metric2")
    test=Matrix.objects.get(name=list_m.selected)
    #print(gt)
    ai=int(math.sqrt(len(gt)))
    shape = ( ai, ai)
    #print(ai)
    gt.shape=shape 
    #print(gt)
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    '''ax.plot([1, 2, 3], 'ro--', markersize=12, markerfacecolor='g')

    # make a translucent scatter collection
    x = np.random.rand(100)
    y = np.random.rand(100)
    area = np.pi * (10 * np.random.rand(100)) ** 2  # 0 to 10 point radii
    c = ax.scatter(x, y, area)
    c.set_alpha(0.5)

    # add some text decoration
    ax.set_title('My first image')
    ax.set_ylabel('Some numbers')
    ax.set_xticks((.2, .4, .6, .8))
    labels = ax.set_xticklabels(('Bill', 'Fred', 'Ted', 'Ed'))

    # To set object properties, you can either iterate over the
    # objects manually, or define you own set command, as in setapi
    # above.
    for label in labels:
        label.set_rotation(45)
        label.set_fontsize(12)'''

    distances=np.array(gt)
    distArray = ssd.squareform(distances)
    fc='b'
    
    linkage_matrix = average(distArray)
    fc= hier.fcluster(linkage_matrix, 6, criterion='maxclust')
   
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
   
    pos = mds.fit_transform(distances)
    xs, ys = pos[:, 0], pos[:, 1]
    ax.scatter(xs, ys, c=fc)
   
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
def MDS_cluster(request, t1):
    t1=int(t1)
    #reamos los datos para representar en el gráfico
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    if(t1==0):
        list_m=Metric.objects.get(name="Metrics")
    elif(t1==1): 
        list_m=Metric.objects.get(name="Metric1")
    elif(t1==2):
        list_m=Metric.objects.get(name="Metric2")
    elif(t1==3): 
        list_m=Metric.objects.get(name="Metric3")
    else:
        list_m=Metric.objects.get(name="Metric4")
    
    
    test=Matrix.objects.get(name=list_m.selected)
    
    gt=np.frombuffer(test.pieces, dtype=np.float64)
    #print(gt)
    ai=int(math.sqrt(len(gt)))
    shape = ( ai, ai)
    #print(ai)
    gt.shape=shape 
    #print(gt)
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    '''ax.plot([1, 2, 3], 'ro--', markersize=12, markerfacecolor='g')

    # make a translucent scatter collection
    x = np.random.rand(100)
    y = np.random.rand(100)
    area = np.pi * (10 * np.random.rand(100)) ** 2  # 0 to 10 point radii
    c = ax.scatter(x, y, area)
    c.set_alpha(0.5)

    # add some text decoration
    ax.set_title('My first image')
    ax.set_ylabel('Some numbers')
    ax.set_xticks((.2, .4, .6, .8))
    labels = ax.set_xticklabels(('Bill', 'Fred', 'Ted', 'Ed'))

    # To set object properties, you can either iterate over the
    # objects manually, or define you own set command, as in setapi
    # above.
    for label in labels:
        label.set_rotation(45)
        label.set_fontsize(12)'''

    distances=np.array(gt)
    distArray = ssd.squareform(distances)
    fc='b'
    
    linkage_matrix = average(distArray)
    fc= hier.fcluster(linkage_matrix, 6, criterion='maxclust')
   
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
   
    pos = mds.fit_transform(distances)
    xs, ys = pos[:, 0], pos[:, 1]
    '''
    trees=[]
    for x in range (0,len(gt)):
        trees.append(str(x +1)) 
    for x, y, name in zip(xs, ys, trees):
        ax.text(x, y, "tree" + name)
    '''
    ax.scatter(xs, ys, c=fc)
   
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response