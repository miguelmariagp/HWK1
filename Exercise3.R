#HKW1: Exercise 3
setwd("C:/Users/ststest/Dropbox/TextAnalysis Grimmer/Day1")
db<-read.csv('db_debate_MP.csv',header=T,stringsAsFactors = F)
head(db)
db$rate_sb_pos<-db$sb_pos/db$non.stop
plot(lowess(db$rate_sb_pos[db$speaker=='OBAMA']~db$ID[db$speaker=='OBAMA']),type='l', col='blue', ylim=c(.04,.11),
     xlab='Time in the debate, by statement', ylab='Proportion of positive statements')
lines(lowess(db$ID[db$speaker=='ROMNEY'],db$rate_sb_pos[db$speaker=='ROMNEY']),type='l', col='red')
lines(lowess(db$ID[db$speaker=='LEHRER'],db$rate_sb_pos[db$speaker=='LEHRER']),type='l', col='green')
legend('top', ncol=3, lty=1,col=c('blue','red','green'), legend=c('Obama   ', 'Romney   ', 'Lehrner   '), bty='n',cex=.8)

#Trends
summary(lm(rate_sb_pos~ID*as.factor(speaker),db))

library(data.table)
tolagdt<-data.table(db)
#Here for the three days sum outcome
tolagdt[, lag.value:=c(NA, speaker[-.N]), by=ID]
db$speaker_lag<-tolagdt$lag.value

summary(lm(rate_sb_pos~speaker*speaker_lag,db))

