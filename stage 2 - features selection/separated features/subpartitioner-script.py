#############################################
#############################################
# SUBPARTITIONER SCRIPT #####################
#############################################
# subpartitions our training data it into 5 independent test/training datasets (5-fold cross validation). these 5 new datasets will be used to check the precision of the feature selection. ############
#############################################
# Jeronimo Barbosa ##########################
# jeronimo.costa [at] mail.mcgill.ca ########
# August 27th 2015 ##########################
#############################################


import os, math, random


#what is the number of subpartitions we want to create?
numberOfSubPartitions = 5
#where is my training data?
path = '/Users/jeronimo/Documents/sbcm 2015/stage 2 - features selection/separated features'
#what is the name of my training data file?
trainingFileName = '/training - 80percent.arff'
#where my new datasets will be saved?
save_path = path +'/subpartitioning training dataset';


#opens my training datafile
file = open(path+trainingFileName, 'r')

#counter
i = 0
#where my relevant data starts
limit=70
#string that will contain my not relevant data (the header of my new arff file)
header = ''
#vector which will store my items
maracatuvirado = []
maracatusolto = []
ciranda = []
coco = []
cavalomarinho = []

#debug
print 'loading training dataset...'

#reads every line in the file
for line in file:
        #if starts reading my dataset items (i am done with the header)
        if (i>limit):
            #if this item is one cavalomarinho
            if 'CavaloMarinho' in line:
                cavalomarinho.append(line)
            #if this item is one ciranda
            if 'Ciranda' in line:
                ciranda.append(line)
            #if this item is one coco
            if 'Coco' in line:
                coco.append(line)
            #if this item is one maracatusolto
            if 'MaracatuSolto' in line:
                maracatusolto.append(line)
            #if this item is one maracatuvirado
            if 'MaracatuVirado' in line:
                maracatuvirado.append(line)
        #if i am reading the header
        else:
            #appends this not relevant line to the header variable
            header = header + line
        #increments counter in order to know which line am I reading
        i=i+1

#how many samples have I collected?
total = len(cavalomarinho)+len(ciranda)+len(coco)+len(maracatusolto)+len(maracatuvirado)
#debug
print str(total) + ' items loaded. they are:'
print '     ' + str(len(cavalomarinho)) + ' cavalomarinho samples loaded'
print '     ' + str(len(ciranda)) + ' ciranda samples loaded'
print '     ' + str(len(coco)) + ' coco samples loaded'
print '     ' + str(len(maracatusolto)) + ' maracatusolto samples loaded'
print '     ' + str(len(maracatuvirado)) + ' maracatuvirado samples loaded'
print

#how big is each subpartition
sizeofSubpartition = int(math.floor(total/numberOfSubPartitions))
#how many items each subpartition must have per genre?
itemsPerGenre = int(math.floor(sizeofSubpartition/5))

#debug
print 'creating subpartitions'

#variables which will store the subpartitions
subpartitions = []
#gathers the items that were not selected in the first round distribution
remainingItems = []

#iterating over the subpartitions
for i in range(numberOfSubPartitions):
    #variable that stores the current subpartition
    currentSubpartiton=[]
    #debug
    print '     creating subpartition ' + str(i+1)
    
    #for each subpartition, gets the ammount of elements needed 
    for j in range(itemsPerGenre):   
        #cavalomarinho - getting a random position for the cavalo marinho vector
        pos = random.randint(0, len(cavalomarinho)-1)
        #print '          pos: ' + str(pos) + ' len(cavalomarinho): ' + str(len(cavalomarinho))
        #getting the cavalo marinho item specified at pos
        item = cavalomarinho.pop(pos);
        #writing this item in the file
        currentSubpartiton.append(item)
        
        #ciranda - getting a random position for the ciranda vector
        pos = random.randint(0, len(ciranda)-1)
        #print '          pos: ' + str(pos) + ' len(ciranda): ' + str(len(ciranda))
        #getting the ciranda item specified at pos
        item = ciranda.pop(pos)
        #writing this item in the file
        currentSubpartiton.append(item)
        
        #coco - getting a random position for the coco vector
        pos = random.randint(0, len(coco)-1)
        #print '          pos: ' + str(pos) + ' len(coco): ' + str(len(coco))
        #getting the coco item specified at pos
        item = coco.pop(pos)
        #writing this item in the file
        currentSubpartiton.append(item)
        
        #maracatusolto - getting a random position for the maracatusolto vector
        pos = random.randint(0, len(maracatusolto)-1)
        #print '          pos: ' + str(pos) + ' len(maracatusolto): ' + str(len(maracatusolto))
        #getting the maracatusolto item specified at pos
        item = maracatusolto.pop(pos)
        #writing this item in the file
        currentSubpartiton.append(item)
        
        #maracatuvirado - getting a random position for the maracatuvirado vector
        pos = random.randint(0, len(maracatuvirado)-1)
        #print '          pos: ' + str(pos) + ' len(maracatuvirado): ' + str(len(maracatuvirado))
        #getting the maracatuvirado item specified at pos
        item = maracatuvirado.pop(pos)
        #writing this item in the file
        currentSubpartiton.append(item)
       
    #adding currentSubpartiton to subpartitions vector
    #print len(currentSubpartiton)
    subpartitions.append(currentSubpartiton)

#gathers the remaining samples in a single 'remainingItems' variable. this items will be redistributed over the subpartitions
remainingItems.extend(cavalomarinho)
remainingItems.extend(ciranda)
remainingItems.extend(coco)
remainingItems.extend(maracatusolto)
remainingItems.extend(maracatuvirado)

#getting how manyof the remaining samples each subpartition will get
howManyRemainingPerSubpartition = int(math.floor(len(remainingItems)/len(subpartitions)))

#debug
print '     restributing the remaining items'

#iterating over the subpartitions
for i in range(numberOfSubPartitions):
    #iterates over the ammount of samples each subpartition should get
    for j in range(howManyRemainingPerSubpartition):
        #gets a random position
        pos = random.randint(0, len(remainingItems)-1)
        #gets this item
        item = remainingItems.pop(pos)
        #appends the item to the arrray
        subpartitions[i].append(item)


#debug  
print
print 'saving arff files'

#iterating over the subpartitions
for i in range(numberOfSubPartitions):
    #sets the place where will save the testing subpartition (eg. 1-testing.arff)
    destination_testing_file_directory  = save_path+'/'+str(i+1)+'-testing.arff'
    #sets the place where will save the tng subpartition (eg. 1-training.arff)
    destination_training_file_directory = save_path+'/'+str(i+1)+'-training.arff'
    #creates testing and trianing output files for this subpartition
    testing_file=open(destination_testing_file_directory, 'w+')
    training_file=open(destination_training_file_directory, 'w+')
    
    #writing the header in both cases
    testing_file.write(header)
    training_file.write(header)
    
    #writing the testing file
    for item in subpartitions[i]:
        testing_file.write(item)
        
    #variables that will store the current training items
    training_items = []

    #preparing the training vector. for this iterate over the partitions again...
    for j in range(numberOfSubPartitions):
        #if this not the current...
        if i != j:
            #unite them together
            training_items.extend(subpartitions[j])
            
    #print 'size of training items:' + str(len(training_items))
    #writing the training file
    for item in training_items:
        training_file.write(item)
    
print 
print 'done!'
    