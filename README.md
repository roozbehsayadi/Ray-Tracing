# Ray Tracing algorithm

## Real-world Mechanisms

How do we see an object with our eyes? As we all know, it's because of the light. Imagine you're standing outside, watching a beautiful flower. Sun rays are constantly coming from the sun. Some of them hit the flower that you're watching. From those rays, some of them reflect and hit your eye. Each ray's color depends on the hitting point on the flower as the flower absorbs rays, and for each of them, it reflects only a portion of it. 

## Simulation

So, this is the real-world mechanism for seeing things, but is it easy to implement?

The answer is no. Sun is constantly shooting rays to the earth. From all of those rays, only a few of them hit our object. Then, only a very few of them reflect into our eyes. So it's computationally very expensive to simulate this process with a machine (one point for mother nature). So how do we do it? 

There's an algorithm called *Backward Tracing*, or as some people prefer to call it, *Eye Tracing*. As its name suggests, it works exactly in the opposite direction. Let's see how that works.

## Backward Tracing

We shoot rays from the eye of the supervisor. It may hit an object, or not. If it does hit an object, then we can say that the supervisor has eye contact with that object. Keep in mind that the closest object is considered. 

The next step is to see if the object has light or not. To achieve this, for every ray we shoot another ray from the hitting point to the light source. If the ray reached the light source, then it has light. Otherwise, it is shadowed.

To get a more natural lighting effect, for every point on an object check if it faces the light source directly or it has angle with light rays. Then you can decide light amount each point gets. 

Another feature for making the render output look more real is reflections; And by reflection I mean seeing a transparent picture of objects inside each other. To achieve this, use recursion on following ray paths. When a ray intersects with a point, calculate its reflection angle and shoot another ray from that point. By recursion you can get its color. Then add the reflection color to original color. Use a coefficient to lower the reflection's effect on color.   

You can checkout output image and list of implemented stuff in the Example Output section below.      

## Running the Code

Required packages are available in the requirements file. You can install them by running ```pip install -r requirements```.

The output will be saved in ```output.png```. You can add or remove spheres by changing the ```objects``` array.

You may notice that rendering an output takes a minute or two on a slower computer. In order to accelerate the rendering process, go to the code, and change the lines where h, w and screen_cor are initialized. You can write a value by yourself or you can use the values that are commented on top of the corresponding lines. 

## Example Output

![Example Output](https://www.dl.dropboxusercontent.com/s/cf49vx3whfackz7/reflection%20coefficients%20bug%20fix.png?dl=0)

Notice that:

* These spheres have the same radius, but they look different from each other.
* A plane!
* Shadow effect. Spheres cast shadow on each other, and also the parts of the spheres that don't face the light are dark.
* Light effect. The points that are facing the light directly are brighter than other points.
* Reflection effect. You can see a transparent reflection of the whole scene in every object. Also each object has its own amount of reflection.
