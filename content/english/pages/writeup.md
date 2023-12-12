---
title: "QEA3 Final Project: Write Up"
meta_title: "Project Overview"
description: "Detailed explanation of the QEA3 Final Project focusing on advanced audio recognition technology."
image: "/images/project-image.png"
draft: false
---

# Motion model:
When trying to find the frequencies of human voice from recordings, we would often run into the issue of harmonics which made the frequency of some time-steps incredibly large. A human’s voice frequency often doesn’t exceed 350 Hz. Knowing this, we needed to filter out frequencies over 350 Hz. The prosthetic hand can be programmed through servo motors which have a range of 0 to 180. Therefore, the voice frequency reader converts the data into a range from 0 to around 350 Hz. The top frequency of 350 Hz is adjustable depending on normal conversational voice frequencies for different people. 

{{< image src="images/audio_data.jpeg" caption="" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title"  webp="false" >}}

# Algorithm development and description:

{{< image src="images/plots/DFT_with_frequencies_in_range.jpg" caption="" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title"  webp="false" >}}

This is an example of raw audio data with amplitude vs time.

{{< image src="images/plots/qea2_image_2.jpg" caption="" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title"  webp="false" >}}

Here is what the normal DFT with frequencies in range looks like. As you can see, the frequency with highest amplitude is at -120 and 120 Hz.

The Fourier transform dissects a waveform signal into a mix of different frequencies, enabling the conversion of a signal between the time and frequency domains. In MATLAB, we employ the fft() function to swiftly perform the Fourier transform on user data in the time domain. Additionally, fftshift() is utilized to reorganize the data, ensuring that the zero-frequency component is positioned at the center of the vector produced by fft().

From here, we developed an algorithm that is able to individually splice the audio file into designated time steps. We found that a timestep around 0.2 seconds worked the best for human voices. In each timestep, we then recorded the frequency with the highest amplitude.

We then ran into an issue where the targeted frequency would occasionally be masked by a high harmonic frequency. Here is an example where the high frequency harmonic around -500 to 500 Hz overshadows the frequency at -120 and 120 Hz which is wanted. In order to do this, we set a threshold frequency value that the top frequency at each given timestamp cannot surpass. If it does, then it will search for the frequency with the highest amplitude within the given threshold numbers.

{{< image src="images/plots/pitch_graph.jpg" caption="" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title"  webp="false" >}}

This data of highest frequency vs time can be used to make a pitch graph. Below are two examples. The first is Anagha's full C major scale, and the second is Khoi's ascending C major scale.

{{< image src="images/plots/Anagha_C_Major_Scale.jpg" caption="" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title"  webp="false" >}}

{{< image src="images/plots/Khoi_Ascending_Scale_Frequency_vs_Time.jpg" caption="" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title"  webp="false" >}}

As you can see, sometimes we still run into other errors where the harmonic is below the highest voice frequency. This spike is not optimal for turning this audio data into control instructions for our prosthetic hand. In order to combat this, a control algorithm was implemented to max out large steps to a given value. In Khoi's case, we maxed out the max step for the servo motor to be 10 ticks. This eliminates any large spikes to when filtered to data that is readable by servos. 

{{< image src="images/plots/khio_servo.jpg" caption="" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title"  webp="false" >}}

As you can see, the controller data ranges from 0 to 180 which is exactly what the servo intakes.

# Proof of concept:
Building on our successful proof of concept in using human voice control for a prosthetic hand, the next steps are crucial for bringing this innovative idea to fruition. We would focus on designing and developing the mechanical and electrical systems, carefully integrating the servo data for precise movement control. This involves selecting appropriate materials and components that ensure durability, responsiveness, and user comfort. Next, we would be optimizing our algorithm to process live audio feeds with minimal latency. This step is critical to ensure real-time responsiveness of the prosthetic hand, making it as intuitive and seamless as possible for the user. The goal is to create a prosthetic hand that not only functions effectively but also feels like a natural extension of the user's body, enhancing their day-to-day life.

