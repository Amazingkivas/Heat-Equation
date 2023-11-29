#pragma once

#include <iostream>
#include <functional>
#include <vector>
#include <fstream>

#include "RunThroughMethod.h"

class HeatEquation {
private:
	real gamma;						// Thermal Conductivity Coefficient
	function<real(real, real)> g;	// External Heat Source
	function<real(real)> phi;		// Initial Temperature Distribution
	function<real(real)> mu1, mu2;	// Boundary Conditions

	real a, b;						// Space Boundaries

	Grid v;							// Solution

public:
	HeatEquation(real coefficient, function<real(real, real)> heat_source, function<real(real)> initial,
		function<real(real)> left_boundary_condtition, function<real(real)> right_boundary_condtition,
		real left_boundray, real right_boundary) : gamma(coefficient), g(heat_source), phi(initial), 
		mu1(left_boundary_condtition), mu2(right_boundary_condtition), a(left_boundray), b(right_boundary) {}

	
	Grid solve_equation(real time, size_t sizes[2]) {
		RunThrough solver(a, b, sizes[0], sizes[1], time, phi, gamma, g, mu1, mu2);
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

// Outfile example: "../../interface/OutputData.csv"
