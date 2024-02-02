#pragma once

#include <iostream>
#include <functional>
#include <vector>
#include <fstream>
#include <string>

#include "RunThroughMethod.h"

class HeatEquation {
private:
	double gamma;             // Thermal Conductivity Coefficient
	BinaryFunction g;         // External Heat Source
	UnaryFunction phi;        // Initial Temperature Distribution
	UnaryFunction mu1, mu2;   // Boundary Conditions
	double a, b;              // Space Boundaries

public:
	HeatEquation(double coefficient, BinaryFunction heat_source, UnaryFunction initial,
		double boundaries[2], UnaryFunction boundary_condtitions[2]) : gamma(coefficient), g(heat_source), phi(initial),
		mu1(boundary_condtitions[0]), mu2(boundary_condtitions[1]), a(boundaries[0]), b(boundaries[1]) {}

	Grid solve_equation(double time, int sizes[2]) {

		double bound_space[2] = { a, b };
		UnaryFunction bound_funcs[2] = { mu1, mu2 };

		RunThrough solver(sizes, time, gamma, g, phi, bound_space, bound_funcs);
		return solver.get_whole_grid();
	}
};

class Writer {
private:
	Grid _to_write;
	double h;
	double tau;

public:
	Writer(Grid& to_write, double h_x, double h_t): h(h_x), tau(h_t) { _to_write = to_write; }

	bool write_grid(char* path);
	bool write_layer(char* path);
};

// Relative path example: "../../interface/OutputData.csv"


bool Writer::write_grid(char* path) {
	std::ofstream fout;
	fout.open(path);
	if (!fout.is_open()) {
		std::cout << "ERROR: Failed to open Out File" << std::endl;
		return false;
	}
	for (int i = 0; i < _to_write.space_size(); ++i) {
		fout << i;
		if (i == _to_write.space_size() - 1) {
			fout << std::endl;
		}
		else {
			fout << ";";
		}
	}
	for (int j = 0; j < _to_write.time_size(); ++j) {
		for (int i = 0; i < _to_write.space_size(); ++i) {

			fout << _to_write(i, j);
			if (i == _to_write.space_size() - 1) {
				fout << std::endl;
			}
			else {
				fout << ";";
			}
		}
	}
	fout.close();
	return true;
}

bool Writer::write_layer(char* path) {
	std::ofstream fout;
	fout.open(path);
	if (!fout.is_open()) {
		std::cout << "ERROR: Failed to open Out File" << std::endl;
		return false;
	}
	int n = _to_write.space_size() - 1;
	int m = _to_write.time_size() - 1;

	for (int i = 0; i <= n; ++i) {
		fout << _to_write(i, m);
		if (i < n) {
			fout << std::endl;
		}
	}
	fout.close();
	return true;
}
