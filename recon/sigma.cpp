#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cmath>
#include <vector>
#include <tuple>
#include <algorithm>

namespace py = pybind11;

double interpolate_legendre(double energy, double mu, const pybind11::dict &legendre_data) {
    auto energies = legendre_data.attr("keys")();
    std::vector<double> energy_list;
    for (auto energy_key : energies) {
        energy_list.push_back(energy_key.cast<double>());
    }

    if (energy < energy_list.front() || energy > energy_list.back()) {
        throw std::runtime_error("Energy out of bounds");
    }

    auto it = std::lower_bound(energy_list.begin(), energy_list.end(), energy);
    if (it == energy_list.end()) {
        --it;
    }
    int idx = std::distance(energy_list.begin(), it);

    double E1 = energy_list[idx];
    double E2 = (idx + 1 < energy_list.size()) ? energy_list[idx + 1] : E1;

    auto coeffs1 = legendre_data[py::float_(E1)].cast<std::vector<double>>();
    auto coeffs2 = legendre_data[py::float_(E2)].cast<std::vector<double>>();

    // Add the first Legendre coefficient (a0 = 1) if it is missing
    coeffs1.insert(coeffs1.begin(), 1.0);
    coeffs2.insert(coeffs2.begin(), 1.0);

    double P1 = 0.0;
    double P2 = 0.0;
    for (size_t l = 0; l < coeffs1.size(); ++l) {
        P1 += coeffs1[l] * std::legendre(l, mu);
    }
    for (size_t l = 0; l < coeffs2.size(); ++l) {
        P2 += coeffs2[l] * std::legendre(l, mu);
    }

    double f = P1 + (energy - E1) / (E2 - E1) * (P2 - P1);
    return f;
}

double interpolate_tabulated(double energy, double mu, const pybind11::dict &tabulated_data) {
    auto energies = tabulated_data.attr("keys")();
    std::vector<double> energy_list;
    for (auto energy_key : energies) {
        energy_list.push_back(energy_key.cast<double>());
    }

    if (energy < energy_list.front() || energy > energy_list.back()) {
        throw std::runtime_error("Energy out of bounds");
    }

    auto it = std::lower_bound(energy_list.begin(), energy_list.end(), energy);
    if (it == energy_list.end()) {
        --it;
    }
    int idx = std::distance(energy_list.begin(), it);

    double E1 = energy_list[idx];
    double E2 = (idx + 1 < energy_list.size()) ? energy_list[idx + 1] : E1;

    auto data1 = tabulated_data[py::float_(E1)].cast<std::tuple<std::vector<double>, std::vector<double>>>();
    auto data2 = tabulated_data[py::float_(E2)].cast<std::tuple<std::vector<double>, std::vector<double>>>();

    const auto &mu_values1 = std::get<0>(data1);
    const auto &f_values1 = std::get<1>(data1);
    const auto &mu_values2 = std::get<0>(data2);
    const auto &f_values2 = std::get<1>(data2);

    auto it_mu1 = std::lower_bound(mu_values1.begin(), mu_values1.end(), mu);
    auto it_mu2 = std::lower_bound(mu_values2.begin(), mu_values2.end(), mu);

    int idx_mu1 = std::distance(mu_values1.begin(), it_mu1);
    int idx_mu2 = std::distance(mu_values2.begin(), it_mu2);

    double mu1 = mu_values1[idx_mu1];
    double mu2 = mu_values2[idx_mu2];

    double f1 = f_values1[idx_mu1];
    double f2 = f_values2[idx_mu2];

    double f_mu1 = f1 + (mu - mu1) / (mu2 - mu1) * (f2 - f1);
    double f_mu2 = f1 + (mu - mu1) / (mu2 - mu1) * (f2 - f1);

    double f = f_mu1 + (energy - E1) / (E2 - E1) * (f_mu2 - f_mu1);
    return f;
}

double sigma(double mu, double energy, const py::dict& legendre_data, const py::dict& tabulated_data, int LTT) {
    if (LTT == 1) {
        return interpolate_legendre(energy, mu, legendre_data);
    } else {
        return interpolate_tabulated(energy, mu, tabulated_data);
    }
}

PYBIND11_MODULE(sigma, m) {
    m.def("sigma", &sigma, "Calculate the scattering distribution",
          py::arg("mu"), py::arg("energy"), py::arg("legendre_data"), py::arg("tabulated_data"), py::arg("LTT"));
}
