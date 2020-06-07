
# TODO Add reflection coefficient in object's properties

import cmath
import numpy as np
import matplotlib.pyplot as plt


def get_new_sphere(position, radius, color, reflection_coefficient):
	return dict(type="sphere", position=np.array(position), radius=radius,
				color=np.array(color), reflection_coefficient=reflection_coefficient)


color_plane_0 = 0.0 * np.ones(3)
color_plane_1 = 1.0 * np.ones(3)


def get_new_plane(point, normal_vector, reflection_coefficient):
	return dict(type="plane", point=np.array(point), normal=np.array(normal_vector),
			reflection_coefficient=reflection_coefficient,
			color=lambda m: (
				color_plane_0 if (int((m[0] if m[0] > 0 else m[0] - 0.5) * 2) % 2)
				== (int((m[2] if m[2] > 0 else m[2] - 0.5) * 2) % 2)
				else color_plane_1))

def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0:
		return v
	return v / norm


objects = [get_new_sphere([0.75, 0.1, 1.0], 0.6, [0.0, 0.0, 1.0], 0.4),
			get_new_sphere([-0.75, 0.1, 2.25], 0.6, [0.5, 0.223, 0.5], 0.3),
			get_new_sphere([-2.75, 0.1, 3.5], 0.6, [1.0, 0.572, 0.184], 0.2),
			get_new_plane([0.0, -0.5, 0.0], [0.0, 1.0, 0.0], 0.35)
		]

# h = 300
# w = 400
h = 1080
w = 1920
image = np.zeros(shape=(h, w, 3))

background_color = 0.0 * np.ones(3)

ambient = 0.1 * np.ones(3)

light_position = np.array([5.0, 5.0, -10.0])
light_color = np.ones(3)

# x0, y0, x1, y1
# screen_cor = [-1, -0.5, 1, 1]
screen_cor = [-1.2, -0.425, 1.2, 0.925]


def get_distance_sphere(ray_o, ray_d, obj):
	Q = ray_o - obj["position"]
	a = np.dot(ray_d, ray_d)
	b = 2 * np.dot(ray_d, Q)
	c = np.dot(Q, Q) - obj["radius"] * obj["radius"]
	d = b * b - 4 * a * c

	if d < 0:
		return np.inf
	if d >= 0:
		t1 = (-b + cmath.sqrt(d)) / (2 * a)
		t2 = (-b - cmath.sqrt(d)) / (2 * a)
		answer = min(t1, t2)
		if answer < 0:
			return np.inf
		return answer


def get_distance_plane(ray_o, ray_d, obj):

	temp = np.dot(ray_d, obj["normal"])
	if np.abs(temp) < 1e-5:
		return np.inf

	OP = obj["point"] - ray_o

	distance = np.real(np.divide(np.dot(OP, obj["normal"]), temp))
	# print(distance)
	if distance < 0:
		return np.inf
	return distance


def get_distance(ray_o, ray_d, obj):
	if obj["type"] == "sphere":
		return get_distance_sphere(ray_o, ray_d, obj)
	if obj["type"] == "plane":
		return get_distance_plane(ray_o, ray_d, obj)


def get_line_point(ray_o, ray_d, distance):
	return ray_o + ray_d * distance


def get_normal_vector(obj, surface_point):
	if obj["type"] == "sphere":
		center = obj["position"]
		return normalize(surface_point - center)
	elif obj["type"] == "plane":
		return obj["normal"]


def get_color(obj, m):
	color = obj["color"]
	if not hasattr(color, '__len__'):
		color = color(m)
	return color


def get_closest_object_properties(ray_o, ray_d):

	min_distance = np.inf
	obj_index = -1

	for i, obj in enumerate(objects):
		distance = get_distance(ray_o, ray_d, obj)
		if distance < min_distance:
			min_distance = distance
			obj_index = i

	return obj_index, min_distance


def is_shadowed(point):
	light_vector = normalize(light_position - point)
	obj_index, distance = get_closest_object_properties(point, light_vector)
	if obj_index == -1:
		return False
	else:
		return True


def get_light_amount(obj_index, point):
	PL = normalize(light_position - point)
	N = get_normal_vector(objects[obj_index], point)
	angle = np.dot(N, PL)
	return np.real(np.clip(angle * np.ones(3), 0.1, 1))


def trace_ray(depth, ray_o, ray_d):

	if depth < 0:
		return np.zeros(3)

	obj_index, distance = get_closest_object_properties(ray_o, ray_d)
	if obj_index == -1:
		return background_color

	obj = objects[obj_index]

	intersect_point = get_line_point(ray_o, ray_d, distance)
	object_normal_vector = get_normal_vector(obj, intersect_point)
	intersect_point = intersect_point + 0.0001 * object_normal_vector

	color = get_color(obj, intersect_point)

	reflection_ray_vector = np.real(ray_d - 2 * np.dot(ray_d, object_normal_vector) * object_normal_vector)
	reflection_ray_color = trace_ray(depth - 1, intersect_point, reflection_ray_vector)

	if is_shadowed(intersect_point):
		return 0.1 * ((1 - obj["reflection_coefficient"]) * color \
					+ reflection_ray_color * obj["reflection_coefficient"])

	color = (1 - obj["reflection_coefficient"]) * color \
			+ reflection_ray_color * obj["reflection_coefficient"]

	toL = normalize(light_position - intersect_point)
	toO = normalize(ray_o - intersect_point)
	color += np.real(np.dot(object_normal_vector, normalize(toL + toO))) ** 50 * light_color

	return np.multiply(color, get_light_amount(obj_index, intersect_point))


def main():

	camera_position = np.array([0.0, 0.25, -1.0])
	camera_direction = np.array([0.0, 0.0, 0.0])

	for i, x in enumerate(np.linspace(screen_cor[0], screen_cor[2], w)):
		for j, y in enumerate(np.linspace(screen_cor[3], screen_cor[1], h)):
			camera_direction[:2] = (x, y)

			ray_o = camera_position
			ray_d = normalize(camera_direction - camera_position)

			trace_answer = trace_ray(3, ray_o, ray_d)
			trace_answer = trace_answer + ambient

			image[j, i, :] = np.clip(trace_answer, 0, 1)

	plt.imsave('output.png', image)


if __name__ == "__main__":
	main()
