#pragma once

#include <iostream>
#include <functional>
#include <vector>
#include <cmath>

#include "RunThroughMethod.h"

class HeatEquation {
private:
	real gamma;						// Thermal Conductivity Coefficient
	function<real(real, real)> g;	// External Heat Source
	function<real(real)> phi;		// Initial Temperature Distribution
	function<real(real)> mu1, mu2;	// Boundary Conditions

	real a, b;						// Space Boundaries

public:
	HeatEquation(real coefficient, function<real(real, real)> heat_source, function<real(real)> initial,
		function<real(real)> left_boundary_condtition, function<real(real)> right_boundary_condtition,
		real left_boundray, real right_boundary) : gamma(coefficient), g(heat_source), phi(initial), 
		mu1(left_boundary_condtition), mu2(right_boundary_condtition), a(left_boundray), b(right_boundary) {}

};
