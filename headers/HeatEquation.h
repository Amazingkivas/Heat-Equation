#pragma once

#include <iostream>
#include <functional>
#include <vector>
#include <fstream>

#include "RunThroughMethod.h"

class HeatEquation {
private:
	real gamma;			// Thermal Conductivity Coefficient
	function<real(real, real)> g;	// External Heat Source
	function<real(real)> phi;	// Initial Temperature Distribution
	function<real(real)> mu1, mu2;	// Boundary Conditions

	real a, b;			// Space Boundaries

	Grid v;				// Solution

public:
	HeatEquation(real coefficient, function<real(real, real)> heat_source, function<real(real)> initial, 
		real boundaries[2], function<real(real)> boundary_condtitions[2]) : gamma(coefficient), g(heat_source), phi(initial),
		mu1(boundary_condtitions[0]), mu2(boundary_condtitions[1]), a(boundaries[0]), b(boundaries[1]) {}

	
	Grid solve_equation(real time, size_t sizes[2]) {

		real bound_space[2] = { a, b };
		function<real(real)> bound_funcs[2] = { mu1, mu2 };

		RunThrough solver(sizes, time, gamma, g, phi, bound_space, bound_funcs);
		return solver.get_whole_grid();
	}
};

class Writer {
private:
	Grid _to_write;

public:
	Writer(Grid& to_write) { _to_write = to_write; }

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
	for (size_t j = 0; j < _to_write.time_size(); ++j) {
		for (size_t i = 0; i < _to_write.space_size(); ++i) {

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
	size_t n = _to_write.space_size() - 1;
	size_t m = _to_write.time_size() - 1;

	for (size_t i = 0; i <= n; ++i) {
		fout << _to_write(i, m);
		if (i < n) {
			fout << std::endl;
		}
	}
	fout.close();
	return true;
}
