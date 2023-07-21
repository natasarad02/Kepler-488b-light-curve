# Simultaneous light curve fitting of Kepler-488 b transit through multiple filters (Petnica project 2021)

In order to collect transit data for B and V filter, I processed photometric images of the Kepler-488 b exoplanet system. The software I used for image processing is called AstroImageJ. 
Light curves were individually fitted through these two filters and then I used them to calculate transit parameters: inclination, semi-major axis length, planet radius and limb darkening coefficients. Eccentricity, orbital period and star radius were fixed. I assumed that the limb darkening coefficients changed according to the linear law.

Then, I fitted the light curves simultaneously (semi-major axis and inclination are identical for both light curves). For simultaneous fitting, I used the Chi-Square method. Depending on the filter, calculated values for planet radius and limb darkening coefficients were different.

Values obtained by simultaneous and individual fitting were compared to each other and then compared to the values from Morton (2016) paper.

## Results


### Individual fitting

|               | Semi-major axis [AU] | Planet radius [Jupiter radii] | Incilination [degrees] | LD coefficient |
| ------------- | -------------------- | ----------------------------- | ---------------------- | -------------- |
| Morton (2016) |     0.0428           |        1.409                  |      /                 |        /       |
|    B filter   |     0.043            |        1.39                   |      84.6              |  0.5           |
|    V filter   |    0.044             |        1.39                   |      84.6              |  0.71          |

![image](https://github.com/natasarad02/kepler-488b/assets/45151070/db24de80-7b2c-442f-91a8-18bb1efc3ee6)



### Simultaneous fitting

|               | Semi-major axis [AU] | Planet radius [Jupiter radii] | Incilination [degrees] | LD coefficient |
| ------------- | -------------------- | ----------------------------- | ---------------------- | -------------- |
| Morton (2016) |     0.0428           |        1.409                  |      /                 |        /       |
|    B filter   |     0.044            |        1.39                   |      84.6              |  0.5           |
|    V filter   |    0.044             |        1.39                   |      84.6              |  0.7           |

![image](https://github.com/natasarad02/kepler-488b/assets/45151070/485df316-c661-4538-b153-2227deab2def)


## Conclusion

Values obtained by simultaneous fitting are almost identical to the parameters obtained by individual fitting. However, in practice, simultaneous fitting would give more precise results, because it gives us the values that simultaneously belong to all datasets (in this case for two filters). The only downside is that it takes too long to fit the data this way.

