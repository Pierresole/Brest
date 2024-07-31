#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>
#include <algorithm>

namespace py = pybind11;

double linear_interpolate(double x, const std::vector<double>& xs, const std::vector<double>& ys) {
    if (xs.size() != ys.size() || xs.size() < 2) {
        throw std::invalid_argument("Vectors xs and ys must be of same size and non-empty.");
    }

    auto it = std::lower_bound(xs.begin(), xs.end(), x);
    if (it == xs.end()) {
        return ys.back();
    } else if (it == xs.begin()) {
        return ys.front();
    }

    size_t idx = std::distance(xs.begin(), it) - 1;
    double x0 = xs[idx], x1 = xs[idx + 1];
    double y0 = ys[idx], y1 = ys[idx + 1];

    return y0 + (x - x0) * (y1 - y0) / (x1 - x0);
}

double log_interpolate(double x, const std::vector<double>& xs, const std::vector<double>& ys) {
    if (xs.size() != ys.size() || xs.size() < 2) {
        throw std::invalid_argument("Vectors xs and ys must be of same size and non-empty.");
    }

    auto it = std::lower_bound(xs.begin(), xs.end(), x);
    if (it == xs.end()) {
        return ys.back();
    } else if (it == xs.begin()) {
        return ys.front();
    }

    size_t idx = std::distance(xs.begin(), it) - 1;
    double x0 = xs[idx], x1 = xs[idx + 1];
    double log_y0 = std::log(ys[idx]), log_y1 = std::log(ys[idx + 1]);

    return std::exp(log_y0 + (x - x0) * (log_y1 - log_y0) / (x1 - x0));
}

double interpolate_legendre(double mu, double energy, const py::dict& legendre_data) {
    std::vector<double> energies;
    for (auto item : legendre_data) {
        energies.push_back(item.first.cast<double>());
    }

    // if (energy < energies.front() || energy > energies.back()) {
    //     throw std::out_of_range("Energy out of bounds.");
    // }

    auto it = std::lower_bound(energies.begin(), energies.end(), energy);
    if (it == energies.end()) {
        it = std::prev(it);
    }
    size_t idx = std::distance(energies.begin(), it);

    double E1 = energies[idx == 0 ? idx : idx - 1];
    double E2 = energies[idx];

    auto coeffs1 = legendre_data[py::float_(E1)].cast<std::vector<double>>();
    auto coeffs2 = legendre_data[py::float_(E2)].cast<std::vector<double>>();

    // Add the first Legendre coefficient a_0 = 1
    coeffs1.insert(coeffs1.begin(), 1.0);
    coeffs2.insert(coeffs2.begin(), 1.0);

    std::vector<double> interpolated_coeffs(coeffs1.size());
    for (size_t i = 0; i < coeffs1.size(); ++i) {
        interpolated_coeffs[i] = linear_interpolate(energy, {E1, E2}, {coeffs1[i], coeffs2[i]});
    }

    double result = 0.0;
    for (size_t l = 0; l < interpolated_coeffs.size(); ++l) {
        result += interpolated_coeffs[l] * std::legendre(l, mu);
    }

    return result;
}

double interpolate_tabulated(double mu, double energy, const py::dict& tabulated_data) {
    std::vector<double> energies;
    for (auto item : tabulated_data) {
        energies.push_back(item.first.cast<double>());
    }

    // if (energy < energies.front() || energy > energies.back()) {
    //     throw std::out_of_range("Energy out of bounds.");
    // }

    auto it = std::lower_bound(energies.begin(), energies.end(), energy);
    if (it == energies.end()) {
        it = std::prev(it);
    }
    size_t idx = std::distance(energies.begin(), it);

    double E1 = energies[idx == 0 ? idx : idx - 1];
    double E2 = energies[idx];

    auto data1 = tabulated_data[py::float_(E1)].cast<std::vector<std::pair<double, double>>>();
    auto data2 = tabulated_data[py::float_(E2)].cast<std::vector<std::pair<double, double>>>();

    std::vector<double> mu_values(data1.size()), f1_values(data1.size()), f2_values(data2.size());
    for (size_t i = 0; i < data1.size(); ++i) {
        mu_values[i] = data1[i].first;
        f1_values[i] = data1[i].second;
        f2_values[i] = data2[i].second;
    }

    double f1 = log_interpolate(mu, mu_values, f1_values);
    double f2 = log_interpolate(mu, mu_values, f2_values);

    return linear_interpolate(energy, {E1, E2}, {f1, f2});
}

double sigma_legendre(double mu, double energy, const py::dict& legendre_data) {
    return interpolate_legendre(mu, energy, legendre_data);
}

double sigma_tabulated(double mu, double energy, const py::dict& tabulated_data) {
    return interpolate_tabulated(mu, energy, tabulated_data);
}

double sigma_combined(double mu, double energy, const py::dict& legendre_data, const py::dict& tabulated_data, double threshold_energy) {
    if (energy <= threshold_energy) {
        return interpolate_legendre(mu, energy, legendre_data);
    } else {
        return interpolate_tabulated(mu, energy, tabulated_data);
    }
}

PYBIND11_MODULE(sigma, m) {
    m.def("sigma_legendre", &sigma_legendre, "Compute sigma using Legendre interpolation",
          py::arg("mu"), py::arg("energy"), py::arg("legendre_data"));
    m.def("sigma_tabulated", &sigma_tabulated, "Compute sigma using Tabulated interpolation",
          py::arg("mu"), py::arg("energy"), py::arg("tabulated_data"));
    m.def("sigma_combined", &sigma_combined, "Compute sigma using combined interpolation",
          py::arg("mu"), py::arg("energy"), py::arg("legendre_data"), py::arg("tabulated_data"), py::arg("threshold_energy"));
}
