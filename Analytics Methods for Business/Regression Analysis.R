# Read data
rawdata <-read.table(file = "Visits.txt",header = TRUE)

#---------------------------------------------------------------------------
# Dispersion test
dispersion_test <- function(x) 
{
  res <- 1-2 * abs((1 - pchisq((sum((x - mean(x))^2)/mean(x)), length(x) - 1))-0.5)
  
  cat("Dispersion test of count data:\n",
      length(x), " data points.\n",
      "Mean: ",mean(x),"\n",
      "Variance: ",var(x),"\n",
      "Probability of being drawn from Poisson distribution: ", 
      round(res, 3),"\n", sep = "")
  
  invisible(res)
}
## sample mean = sample variance => follow Poisson distribution
## p value < 0.05 reject H0 => doesn't follow Poisson distribution
## p value > 0.05 accept H0 => follow Poisson distribution.

dispersion_test(rawdata$visits)

library(AER)
dispersiontest(glmpoi)

library(DHARMa)
testDispersion(glmpoi)
#---------------------------------------------------------------------------
# Run poisson regression model
glmpoi <- glm(visits ~ ., data = rawdata, family = poisson)
summary(glmpoi)

# Residual analysis
par(mar = c(1, 1, 1, 1))
plot(glmpoi)

# Drop insignificant varaibles 
glmpoi_2 <- glm(visits ~ gender + income + illness + reduced +
                  health + freepoor, data = rawdata, family = poisson)
summary(glmpoi_2)


# Run quasi-poisson regression model
glmquasi <- glm(visits ~ ., data = rawdata, family = quasipoisson)
summary(glmquasi)

## Dispersion parameter = 1.32 suggesting a little bit over-dispersion

# Run nb
m1 <- glm.nb(visits ~., data = rawdata)
summary(m1)

m2 <- glm.nb(visits ~ gender + illness + reduced + health + freepoor, data = Visits)
summary(m2)

# ANOVA
anova(glmquasi, m2, test="Chisq")




