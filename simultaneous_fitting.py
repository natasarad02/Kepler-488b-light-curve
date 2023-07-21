import numpy as np
import matplotlib.pyplot as plt
import batman

tB, fluxB, dfluxB = np.loadtxt("B-data.csv", unpack=True, skiprows=1, usecols=[0, 1, 2], delimiter=',')

middle_indextB = int((len(tB) - 1) / 2)

tB = tB - tB[middle_indextB]  # - 0.025 + 0.01

plt.errorbar(tB, fluxB, yerr=dfluxB, fmt='o', label="B filter", color = 'black')


tV, fluxV, dfluxV = np.loadtxt("V-data.csv", unpack=True, skiprows=1, usecols=[0, 1, 2], delimiter=',')
fluxV = np.delete(fluxV, [0, 1])
dfluxV = np.delete(dfluxV, [0, 1])
tV = np.delete(tV, [0, 1])

middle_indextV = int((len(tV) - 1) / 2)

tV = tV - tV[middle_indextV]  # - 0.025 + 0.02

plt.errorbar(tV, fluxV, yerr=dfluxV, fmt='o', label="V filter", color='grey')


params = batman.TransitParams()

a = np.arange(0.038, 0.051, 0.001)
rp1 = np.arange(1.3, 1.5, 0.02)
rp2 = np.arange(1.3, 1.5, 0.02)
inc = np.arange(84, 90, 0.2)

uB = np.arange(0.7, 0.83, 0.01)
uV = np.arange(0.5, 0.83, 0.01)

offsetB = np.arange(0.005, 0.010, 0.001)
offsetV = np.arange(0.005, 0.010, 0.001)

def ModelLin(t1, t2, a, rp1, rp2, inc, u1, u2, offsetB, offsetV):
    p0 = 3.1
    params.t0 = 0.  # planet is exactly between the star and the observer
    params.per = p0  # orbital period
    params.inc = inc  # inclination in degrees
    params.ecc = 0.0  # eccentricity
    params.w = 0  # longitude in degrees

    # First model
    params.u = [u1]  # limb darkening coefficients
    params.limb_dark = "linear"  # limb darkening model
    params.rp = rp1 * 0.0921  # planet radius in stellar radii
    params.a = a * 197.277  # semi-major axis in stellar radii
    m = batman.TransitModel(params, t1)
    flux_model1 = m.light_curve(params)

    # Second model
    params.u = [u2] # limb darkening coefficients
    params.limb_dark = "linear"  # limb darkening model
    params.rp = rp2 * 0.0921
    m = batman.TransitModel(params, t2)
    flux_model2 = m.light_curve(params)
    return (np.array(flux_model1) + offsetB), (np.array(flux_model2) + offsetV)


def Chi2Lin(x1, x2, t1, t2, a, rp1, rp2, inc, u1, u2,  offsetB, offsetV, d1, d2):
    M1, M2 = ModelLin(t1, t2, a, rp1, rp2, inc, u1, u2, offsetB, offsetV)
    x21 = np.sum(((x1 - M1) / d1) ** 2)
    x22 = np.sum(((x2 - M2) / d2) ** 2)
    return (x21 + x22)


x2 = []

nr = 1.0/(len(a)*len(inc)*len(rp1)*len(rp2))
procenat = 0

for i in range(len(a)):
    for j in range(len(inc)):
        for k in range(len(rp1)):
            for p in range(len(rp2)):
                procenat += nr
                print(str(procenat * 100) + "%")

                for r in range(len(uB)):
                    for q in range(len(uV)):
                        for m in range(len(offsetB)):
                            for n in range(len(offsetV)):
                                x2.append(Chi2Lin(fluxB, fluxV, tB, tV, a[i], rp1[k], rp2[p], inc[j], uB[r], uV[q], offsetB[m], offsetV[n], dfluxB, dfluxV))



x2 = np.array(x2)
x2_matrix = np.reshape(x2, (len(a), len(inc), len(rp1), len(rp2), len(uB), len(uV), len(offsetB), len(offsetV)))

index = np.argmin(x2_matrix)
ind1, ind2, ind3, ind4, ind5, ind6, ind7, ind8  = np.unravel_index(index, (len(a), len(inc), len(rp1), len(rp2), len(uB),  len(uV),  len(offsetB), len(offsetV)), order='C')


flux_model1, flux_model2 = ModelLin(tB, tV, a[ind1], rp1[ind3], rp2[ind4], inc[ind2], uB[ind5], uV[ind6], offsetB[ind7], offsetV[ind8])
print(a[ind1], rp1[ind3], rp2[ind4], inc[ind2], uB[ind5], uV[ind6], offsetB[ind7], offsetV[ind8])



plt.plot(tB, flux_model1, 'red')
plt.plot(tV, flux_model2, 'orange')
plt.title("Light curve of Kepler-488 b transit (B and V filter)")
plt.xlabel("Transit duration (hours)")
plt.ylabel("Relative flux")


plt.legend()
plt.show()