
import cmath
import numpy as np
import matplotlib.pyplot as plt


def get_new_sphere(position, radius, color):
	return dict(position=np.array(position), radius=radius, color=np.array(color))


def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0:
		return v
	return v / norm


objects = [get_new_sphere([0.75, 0.1, 1.0], 0.6, [0.0, 0.0, 1.0]),
			get_new_sphere([-0.75, 0.1, 2.25], 0.6, [0.5, 0.223, 0.5]),
			get_new_sphere([-2.75, 0.1, 3.5], 0.6, [1.0, 0.572, 0.184])]

# objects = [get_new_sphere([1.5, 0.0, 4.0], 0.5, [0.0, 0.0, 1.0]),
# 		   get_new_sphere([-2.0, 0.0, 4.0], 2.0, [0.0, 1.0, 0.0])]

# objects = [get_new_sphere([0.0, 0.0, 2.0], 0.1, [0.0, 0.0, 1.0])]

h = 300
w = 400
image = np.zeros(shape=(h, w, 3))

background_color = 0.1 * np.ones(3)

ambient = 0.1 * np.ones(3)

light_position = np.array([5.0, 1.0, -10.0])
# light_position = np.array([5, 0.0, 4.0])
light_color = np.ones(3)

# x0, y0, x1, y1
screen_cor = [-1, -0.5, 1, 1]


def get_distance(ray_o, ray_d, obj):
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


def get_line_point(ray_o, ray_d, distance):
	return ray_o + ray_d * distance


def get_normal_vector(obj, surface_point):
	center = obj["position"]
	return normalize(surface_point - center)


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


def trace_ray(ray_o, ray_d):

	obj_index, distance = get_closest_object_properties(ray_o, ray_d)
	if obj_index == -1:
		return background_color

	intersect_point = get_line_point(ray_o, ray_d, distance)
	object_normal_vector = get_normal_vector(objects[obj_index], intersect_point)
	intersect_point = intersect_point + 0.0001 * object_normal_vector

	if is_shadowed(intersect_point):
		return objects[obj_index]["color"] * 0.1

	return objects[obj_index]["color"]


def main():

	camera_position = np.array([0.0, 0.35, -1.0])
	camera_direction = np.array([0.0, 0.0, 0.0])

	for i, x in enumerate(np.linspace(screen_cor[0], screen_cor[2], w)):
		for j, y in enumerate(np.linspace(screen_cor[1], screen_cor[3], h)):
			camera_direction[:2] = (x, y)

			ray_o = camera_position
			ray_d = normalize(camera_direction - camera_position)

			trace_answer = trace_ray(ray_o, ray_d)
			trace_answer = trace_answer + ambient

			image[j, i, :] = np.clip(trace_answer, 0, 1)

	plt.imsave('output.png', image)


if __name__ == "__main__":
	main()
