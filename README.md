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

## Implementations

In this release, observer can view the spheres and also the spheres cast a shadow on themselves on each other if needed.   

## Running the Code

Required packages are available in the requirements file. You can install them by running ```pip install -r requirements```.

The output will be saved in ```output.png```. You can add or remove spheres by changing the ```objects``` array.

## Example Output

![Example Output](https://www.dl.dropboxusercontent.com/s/9b9yc1un7eh81qr/release-2.png?dl=0)

*These spheres have the same radius, but they look different from each other. You can also see the dark parts of each sphere.*
