# import required libraries
library(sp)
library(gstat)
library(stats)
library(ggplot2)
library(grid)
library(gridExtra)

# import local functions
source('~/Dropbox/Current/krg_ver1/nscore.R')

# read data
# cwd <- "../simulations/testing/2601_801_1601-seed1-a005-mu0_0.225_deltau_5mpa_h1_eq_1_co_1.0mpa_dc_s2/"
args = commandArgs(trailingOnly = TRUE)
if (length(args)==0) {
  stop("working directory of simulation must be supplied.", call.=FALSE)
} else if (length(args) == 1) {
  cwd = args[1]
}
sim = read.csv( paste(cwd, "/data/data_sampled.csv", sep=""), 
               header=TRUE )

# define coordinates for simulated data
coordinates(sim) = ~x+z

# normal score transform
sim.slip.sc <- nscore(sim$sum)
sim.psv.sc <- nscore(sim$psv)
sim.mu0.sc <- nscore(sim$mu0)
sim.vrup.sc <- nscore(sim$vrup)

sim$slip.sc <- sim.slip.sc$nscore
sim$psv.sc <- sim.psv.sc$nscore
sim$mu0.sc <- sim.mu0.sc$nscore
sim$vrup.sc <- sim.vrup.sc$nscore

# gstat object data used to fit lmc
sim.g <- gstat(id='slip', formula=slip.sc~1, data=sim)
sim.g <- gstat(sim.g, 'psv', psv.sc~1, sim)
sim.g <- gstat(sim.g, 'vrup', vrup.sc~1, sim)
sim.g <- gstat(sim.g, 'mu0', mu0.sc~1, sim)

# estimate variograms and co-variograms
var <- variogram(sim.g, cressie = TRUE, width=500)

# plot variograms so cumbersome
# split for easy access
variograms <- split(var, f=var$id)

# save variograms as individual csv files in folder variograms
dir.create( paste(cwd, "data/vario", sep="") )
for (name in names(variograms)) {
  filename = paste(cwd, "data/vario/", name, ".csv", sep="")
  # print(filename)
  write.csv(variograms[name], file = filename)
  # print(variograms[name])
  # print(name)
}

# define layout
lay <- rbind(c(1,NA,NA,NA), c(2,3,NA,NA),c(4,5,6,NA),c(7,8,9,10))

# define plots 
p1 <- ggplot(data = variograms$slip, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("slip")

p2 <- ggplot(data = variograms$slip.psv, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("slip.psv")

p3 <- ggplot(data = variograms$psv, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("psv")

p4 <- ggplot(data = variograms$slip.vrup, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("slip.vrup")

p5 <- ggplot(data = variograms$psv.vrup, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("vrup.psv")

p6 <- ggplot(data = variograms$vrup, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("vrup")

p7 <- ggplot(data = variograms$slip.mu0, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("slip.mu0")

p8 <- ggplot(data = variograms$psv.mu0, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("psv.mu0")

p9 <- ggplot(data = variograms$vrup.mu0, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("vrup.mu0")

p10 <- ggplot(data = variograms$mu0, aes(x=dist, y=gamma)) + geom_point() + 
  theme( axis.title.x = element_blank(),
         axis.title.y = element_blank()) + ggtitle("mu0")

# write out variogram in some readable format, preferably csv 
grd <- grid.arrange(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10, layout_matrix=lay, bottom="dist", left="gamma")
ggsave( paste(cwd, "figs/vario.pdf", sep=""), grd )
