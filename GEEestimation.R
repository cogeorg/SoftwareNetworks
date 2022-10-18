# Estimate community structure with Graph Encoder Embedding (GEE)

# functions needed for estimation

suppressMessages(require(igraph))
suppressMessages(require(Matrix))
##suppressMessages(require(irlba))
suppressMessages(require(mclust))
##suppressMessages(require(ClustR))
##suppressMessages(require(gmmase))
suppressMessages(require(wordspace))
options(warn =-1)

## Args:
##   X: either n*n adjacency matrix, or s*2 or s*3 (unweighted or weighted) edgelist. Vertex size should be >10.
##   Y: size n*1 Class label vector, or a positive integer for number of classes, or a range of potential cluster size, i.e., [2,10]. 
##      In case of partial known labels, Y should be n*1 with unknown class label set to non-positive number (say 0 or -1).
##      When there is no known label, set Y to the desired K, or a range of potential K (ideally n/max(K)>15)
##   Laplacian specifies whether to uses graph Laplacian or adjacency matrix; 
##   Correlation specifies whether to use angle metric or Euclidean metric;
##   DiagA = true augment all diagonal entries by +1 (i.e., add self-loop to edgelist);
##   Three options for clustering: Replicates denotes the number of replicates for clustering, 
##                               MaxIter denotes the max iteration within each replicate for encoder embedding,
##                               MaxIterK denotes the max iteration used within kmeans.
##
## Return:
##   result: Encoder Embedding Z of size n*k, Y is the final label, W is the encoder projection matrix. 
##           For clustering, also output the GEE Clustering Score (called Minimal Rank Index in paper);
##           For classification, also output indT as the index of known labels.
##
## Reference:
##   C. Shen and Q. Wang and C. E. Priebe, "Graph Encoder Embedding", 2022. 
##   C. Shen and C. E. Priebe and Y. Park, "Graph Encoder Embedding for Refined Clustering", 2023.

## Main Function
## X=as.matrix(get.data.frame(g));
GraphEncoder <- function(X, Y=c(2:5), Laplacian = FALSE, DiagA = TRUE, Correlation = TRUE, MaxIter=30, MaxIterK=3, Replicates=3) {
  
  s=dim(X);
  t=s[2];s=s[1];
  
  if (s==t){ #convert adjacency matrix to edgelist
    X = graph.adjacency(X,weighted=TRUE);
    n=vcount(X);
    X = as.matrix(get.data.frame(X));
  }
  if (t==2){
    X=cbind(X,matrix(1, nrow = s, ncol = 1));
  } 
  n = max(max(X[,1:2]))[1];
  if (DiagA==TRUE){
    XNew=cbind(1:n,1:n,1);
    X=rbind(X,XNew);
  }
  
  ## partial or full known labels when label size matches vertex size, do embedding / classification directly
  if (length(Y)==n){
    result = GraphEncoderEmbed(X, Y, n, Laplacian,Correlation);
    GCS=0;Y=result$Y;indT=result$indT;
  } else {
    ## otherwise do clustering
    indT=matrix(0, nrow = n, ncol = 1);
    K=Y;
    ## when a given cluster size is specified
    if (length(K)==1){ #clustering
      result=GraphEncoderCluster(X,K,n,Laplacian,Correlation, MaxIter, MaxIterK, Replicates);
      Y=result$Y;GCS=result$GCS;
    } else {
      ## when a range of cluster size is specified
      K=sort(K); # ensure increasing K
      if (length(K)<n/2 & max(K)<max(n/2,10)){
        tmpGCS=1;Z=0;W=0;GCS = rep(0, length(K));
        for (r in 1:length(K)){
          resTmp = GraphEncoderCluster(X,K[r],n,Laplacian,Correlation, MaxIter, MaxIterK, Replicates);
          tmp=resTmp$GCS;
          GCS[r]=tmp;
          if (tmp<=tmpGCS){
            tmpGCS=tmp;
            result=resTmp;
          }
        }
        Y=result$Y;
      }
    }
  }
  result = list(Z = result$Z, Y = Y, W = result$W, GCS=GCS, indT=indT);
  return(result)
}

## Clustering Function
GraphEncoderCluster <- function(X, K, n, Laplacian = FALSE, Correlation = TRUE, MaxIter=50, MaxIterK=5, Replicates=3) {
  GCS = 1;
  #ariv = rep(0, MaxIter);
  for (rep in 1:Replicates){
    Y2 = matrix(sample(K,n,rep=T), n, 1);
    for (r in 1:MaxIter) {
      cat("Replicate =",rep,"; Iteration =",r)
      resTmp = GraphEncoderEmbed(X, Y2, n, Laplacian, Correlation);
      #grp = KMeans_rcpp(resTmp$Z, K); 
      #Y3=grp$clusters
      grp = kmeans(resTmp$Z, K, iter.max = MaxIterK); 
      Y3 = grp$cluster;
      #grp = Mclust(resTmp$Z, verbose = FALSE);
      #Y3 = grp$classification;
      #ariv[i] = adjustedRandIndex(Y2, Y3);
      Y3 = matrix(Y3, n, 1);
      ari_temp = adjustedRandIndex(Y2, Y3);
      cat("; ARI = ", ari_temp, "\n")
      if (ari_temp == 1) {
        break
      } else {
        Y2 = matrix(Y3, n, 1);
      }
    }
    resTmp = GraphEncoderEmbed(X, Y3, n, Laplacian, Correlation); # Re-Embed using final label Y3
    tmpGCS = calculateGCS(resTmp$Z,Y3,n,K);
    if (tmpGCS<=GCS){
      GCS=tmpGCS;
      Y=Y3;
      result=resTmp;
    }
  }
  result = list(Z = result$Z, Y = Y, W = result$W, GCS=GCS);
  return(result)
}

## Embedding Function
GraphEncoderEmbed <- function(X, Y, n, Laplacian = FALSE, Correlation = TRUE) {
  indT=(Y>0);
  Y1=Y[indT,];
  s=dim(X)[1];
  tmp=unique(Y1);
  k=max(tmp);
  ##X=as.matrix(X,s,t);
  ##Y=as.matrix(Y,n,1);
  ##Y[indT]=Ytmp;
  
  nk=matrix(0, nrow = 1, ncol = k);
  W=matrix(0, nrow = n, ncol = k);
  indS=matrix(0, nrow = n, ncol = k);
  
  for (i in 1:k) {
    ind=(Y==i);
    nk[i]=sum(ind);
    W[ind,i]=1/nk[i];
    indS[,i]=ind;
  }
  
  if (Laplacian==TRUE){
    D=array(0, dim = c(n, 1));
    for (i in 1:s){
      a=X[i,1];
      b=X[i,2];
      c=X[i,3];
      D[a]=D[a]+c;
      if (a!=b){
        D[b]=D[b]+c;
      }
    }
    D=D.^-0.5;
    for (i in 1:s){
      X[i,3]=X[i,3]*D[X[i,1]]*D[X[i,2]];
    }
  }
  
  Z=matrix(0, nrow = n, ncol = k);
  for (i in 1:s) {
    a=X[i,1];
    b=X[i,2];
    c=Y[a];
    d=Y[b];
    e=X[i,3];
    if (d > 0){
      Z[a,d]=Z[a,d]+W[b,d]*e;
    }
    if (c > 0 & a!=b){
      Z[b,c]=Z[b,c]+W[a,c]*e;
    }
  }
  
  if (Correlation==TRUE){
    Z=normalize.rows(Z, method = "euclidean", p = 2);
    Z[is.na(Z)] = 0;
  }
  result = list(Z = Z, Y = Y, W = W, indT = indT)
  return(result)
}

## Compute GEE Clustering Score (minimal rank index)
calculateGCS <- function(Zt, Y3, n, K) {
  D=matrix(0, nrow = n, ncol = K); #between-cluster squared distance from each observation to the each center
  for (i in 1:K){
    D[1:n,i]=t(rowNorms(Zt-matrix(colMeans(Zt[Y3==i,]), nrow=n, ncol=K, byrow=TRUE)));
  }
  tmpIdx=apply(D, 1, which.min);
  tmpGCS=mean(tmpIdx!=Y3);
  return(tmpGCS)
}







# Run estimation
pacman::p_load(irlba, igraph, mclust, Matrix, lubridate, scales, vegan, broom, tidyverse, gmmase, ggrepel)

suppressMessages(require(igraph))
suppressMessages(require(mclust))
suppressMessages(require(tidyverse))
suppressMessages(require(doParallel))
registerDoParallel(detectCores()/2)

# # Build a 3-SBM
# nk <- 200
# K <- 4 #10
# nrho <- rep(nk, K)
# n <- sum(nrho)
# set.seed(1234)
# 
# #B <- c(.01,.05,.07,.1,.12,.15,.18,.2,.22, .25) %*% t(c(.01,.05,.07,.1,.12,.15,.18,.2,.22, .25))
# #B <- matrix(c(0.1,0.01,0.02,
# #              0.01,0.05,0.03,
# #              0.02,0.03,0.02), nrow = 3, ncol = 3)
# 
# #B <- rbind(c(.1,.01,.05),
# #           c(.01,.1,.025),
# #           c(.05,.025,.15))
# B <- rbind(c(.1,.01,.015,0.02),
#            c(.01,.1,.025, .005),
#            c(.015,.025,.15, .01),
#            c(.02,.005,.01,.1))
# rho <- rep(1/K,K)
# Y <- rep(1:K, each=n/K)
# 
# 
# g <- sample_sbm(n, B, nrho); A <- g[]
# #km1 <- GraphEncoder(A, K)
# 
# 
# km1 <- GraphEncoder(A, K, Replicates = 1, MaxIter = 10000)
# 
# adjustedRandIndex(km1$Y,Y)
# 


# estimation with real data
set.seed(1234)

# folders and files
#datafolder <- "/Users/Angelo_1/Dropbox/SoftwareNetworks/Data/npm/"   #macbook14
datafolder <- "C:/Users/amele1/Dropbox/SoftwareNetworks/Data/npm/"  # respcnew
filename <- "enc_sampled-0.001_dependencies_npm-merged-lcc.dat"
file_to_use <- paste(datafolder,filename,sep = "")

# extract data
el <- read_delim(file_to_use, delim = " ")
el
head(el)
tail(el)
max(el)

# since it was created with python, need to add 1 to each node id 
el <- el + 1

# create edgelist
net <- graph_from_edgelist(as.matrix(el), directed = FALSE)

A <- net[]

# let's choose K=10
K <- 4
estimation <- GraphEncoder(A, K, Replicates = 1, MaxIter = 1000)



table(estimation$Y)

