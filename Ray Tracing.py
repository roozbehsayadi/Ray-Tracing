
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

h = 300
w = 400
image = np.zeros(shape=(h, w, 3))

background_color = 0.1 * np.ones(3)

# x0, y0, x1, y1
screen_cor = [-1, -0.75, 1, 0.75]


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
		return min(t1, t2)


def trace_ray(ray_o, ray_d):

	min_distance = np.inf
	obj_index = 0
	for i, obj in enumerate(objects):
		distance = get_distance(ray_o, ray_d, obj)
		if distance < min_distance:
			min_distance = distance
			obj_index = i

	if min_distance == np.inf:
		return background_color

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

			image[j, i, :] = trace_answer

	plt.imsave('output.png', image)


if __name__ == "__main__":
	main()
