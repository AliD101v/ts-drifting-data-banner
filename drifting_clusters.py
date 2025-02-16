import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def generate_sinewave_points(width, height,
                             n_points=3000,
                             random_seed=42,
                             amplitude_factor=0.3,
                             scatter_factor=0.02):
    """
    Generate points along a sine wave from left to right.

    Parameters
    ----------
    width, height : int
        Dimensions of the background image (or desired plotting area).
    n_points : int
        How many points to generate.
    random_seed : int or None
        Seed for reproducibility. If None, random every time.
    amplitude_factor : float
        Controls the vertical amplitude of the sine wave (fraction of image height).
    scatter_factor : float
        Controls how far points can scatter around the wave, as a fraction of width/height.

    Each point has a parameter t in [0,1]:
      x(t) = x_start + t * (x_end - x_start)
      phase(t) = 2*pi * t
      y(t) = y_center + amplitude * sin(phase(t))

    We add Gaussian noise with std = (scatter_factor * width) in x
                                and (scatter_factor * height) in y,
    so points form a loose cluster around the wave.
    """

    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Define left->right boundaries
    x_start = 0.1 * width
    x_end   = 0.9 * width
    
    # Vertical center
    y_center = 0.5 * height
    
    # Amplitude of the wave
    amplitude = amplitude_factor * height
    
    # Prepare arrays
    points = np.zeros((n_points, 2))
    t_values = np.random.rand(n_points)  # random t in [0,1]
    
    # Noise scale: scatter factor
    noise_scale_x = scatter_factor * width
    noise_scale_y = scatter_factor * height
    
    for i in range(n_points):
        t = t_values[i]
        
        # X coordinate moves linearly across the banner
        x_t = x_start + t * (x_end - x_start)
        
        # Phase from 0 -> 2*pi
        phase_t = 2.0 * np.pi * t
        
        # Sine wave
        y_t = y_center + amplitude * np.sin(phase_t)
        
        # Add some noise around the wave
        x_noise = np.random.normal(0, noise_scale_x)
        y_noise = np.random.normal(0, noise_scale_y)
        
        points[i] = [x_t + x_noise, y_t + y_noise]
    
    return points, t_values

def main():
    # Try to load "bg.png". If not found, we'll default to a white background.
    bg_file = "bg.png"
    bg_img = None
    if os.path.isfile(bg_file):
        bg_img = mpimg.imread(bg_file)  # Found the file
    
    # If we have a background image, get its dimensions; otherwise define a "virtual" size.
    if bg_img is not None:
        img_height, img_width = bg_img.shape[:2]
    else:
        # Define a default dimension for our plain white canvas if no image is provided
        img_width, img_height = 1584, 396  # e.g., LinkedIn recommended ratio
    
    # Prepare the figure
    base_width_in = 15.84  # 15.84" wide
    ratio = img_height / img_width
    fig_height_in = base_width_in * ratio
    dpi_val = 300
    scatter_factor = 0.05 # defaults to 5% of width/height
    
    fig, ax = plt.subplots(figsize=(base_width_in, fig_height_in), dpi=dpi_val)
    
    # If a background image exists, display it
    if bg_img is not None:
        ax.imshow(bg_img,
                  extent=[0, img_width, 0, img_height],
                  origin='upper',
                  aspect='auto')
    else:
        # No background image, so just ensure the facecolor is white
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        # We won't do an imshow() here

    # Generate the sine wave points
    points, t_values = generate_sinewave_points(
        width=img_width,
        height=img_height,
        n_points=3000,
        random_seed=42,
        amplitude_factor=0.3,   # wave height relative to image height
        scatter_factor=scatter_factor     # scatter around the wave
    )
    
    # Scatter the points, color by t-values
    ax.scatter(points[:, 0],
               points[:, 1],
               c=t_values,
               cmap='viridis',  # or 'plasma', 'magma', etc.
               alpha=0.7,
               s=20,
               edgecolor='none')
    
    # Remove axes for a clean look
    ax.set_axis_off()
    
    # Align axes with the full area
    ax.set_xlim(0, img_width)
    ax.set_ylim(img_height, 0)
    
    # Save the final banner
    plt.savefig("banner.png", bbox_inches='tight', pad_inches=0)
    plt.close(fig)

if __name__ == "__main__":
    main()
