#define _USE_MATH_DEFINES

#include <iostream>
#include "HeatEquation.h"
#include "RunThroughMethod.h"
#include <cmath>

int main(int argc, char* argv[]) {
	real gamma = 2.0;
	function<real(real, real)> g = [](real x, real t) { return exp(-t) * sin(7 * M_PI * x) + 1; };
	function<real(real)> phi = [](real x) { return 1 - x * x; };
	function<real(real)> mu1 = [](real t) { return cos(t); };
	function<real(real)> mu2 = [](real t) { return sin(4 * t); };
	real a = 0.0;
	real b = 1.0;

	function<real(real)> boundary_conditions_funcs[2] = { mu1, mu2 };
	real space_boundaries[2] = { a, b };

	HeatEquation eq(gamma, g, phi, space_boundaries, boundary_conditions_funcs);
	Grid solution;

	size_t sizes[2] = { 100, 100 };
	solution = eq.solve_equation(5, sizes);
	Writer write(solution);
	
	if(!write.write_grid("../../interface/OutputData.csv")) {
		std::cout << "ERROR: Failed to open OutputData.csv";
		return 1;
	}
	
	if (!write.write_layer("../../interface/OutLayerData.txt")) {
		std::cout << "ERROR: Failed to open OutLayerData.txt";
		return 1;
	}
	return 0;
}
