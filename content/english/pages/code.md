---
title: "QEA3 Final Project: Code"
meta_title: "Project Overview"
description: "Detailed explanation of the QEA3 Final Project focusing on advanced audio recognition technology."
image: "/images/project-image.png"
draft: false
---
```MATLAB
clear
%load handel
file_path = 'Khoi scale.m4a';
[y, fs] = audioread(file_path);
time = length(y)./fs; % time in seconds
T = 1/fs;           % Sampling period
t = 0:T:time; 
t = t(1:end-1);
y = y(:, 1);
% lowpass(y,500,fs)
% y = lowpass(y,500, fs);
sound(y, fs) %

% file_path = 'anagha2.m4a';
% [y2, fs2] = audioread(file_path);
% time2 = length(y2)./fs2; % time in seconds
% T2 = 1/fs2;           % Sampling period
% t2 = 0:T2:time2; 
% t2 = t2(1:end-1);
% y2 = y2(:, 1);
% [y_low,d] = lowpass(y2,450, fs2);
% figure
% plot(t2, y_low, 'r--')
% xlabel('Time (s)')
% ylabel('Amplitude')
% hold on;

plot(t, y,'b')
xlabel('Time (s)')
ylabel('Amplitude')
hold off;

time_step = .2; % in seconds
threshold = 277;
max_step = 20;
steps = time/time_step;
round_step = floor(steps);
index = round(length(y)/ steps);
start_index = 1;
end_index = 1;
highest_freq = [];

for i = 1:round_step
   
    end_index = end_index + index;
    start_index = end_index - index;
    segment = y(start_index : end_index-1);
    n = length(segment);
    y0 = fftshift(fft(segment));         % shift y values
    f0 = (-n/2:n/2-1)*(fs/n); % 0-centered frequency range
    amp = abs(y0).^2/n;    % 0-centered amplitude
%     if i == 4
%         figure
%         plot(f0,amp);
%         xlabel('Frequency')
%         ylabel('Amplitude')
%         xlim([-.1e4, .1e4])
%         hold off;
%     end
    [amp_val, amp_indx] = sort(amp,'descend');

    z = 1;
    while true
        freq_threshold = f0(amp_indx(2 * z));
        if freq_threshold < threshold
            highest_freq(1, i) = f0(amp_indx(2 * z));
            break;  % Exit the loop when the condition is met
        end
        z = z + 1;
    end
    highest_freq(2, i) = time_step * i;
end

figure
plot(highest_freq(2,:), highest_freq(1,:))
    title("Khoi Ascending C Major Scale Frequency vs Time")
    xlabel('Time (s)')
    ylabel('Frequency (Hz)')
%     ylim([0, 1000])

%Reference algorithm

%figure()
%hold off
%pitch(y, fs)

distance = [];

distance(1) = (highest_freq(1,1) - 130)/15

for i = 2:length(highest_freq)      
    if highest_freq(1, i) - highest_freq(1,i - 1) > 50
        distance(i)  = ((highest_freq(1, i - 1) + max_step))/20
        print("hi")
    else
     distance(i) = (highest_freq(1,i))/20;
    end 
end

figure()
plot(highest_freq(2,:), distance)
 title("Khoi Scale Height vs Time")
    xlabel('Time (s)')
    ylabel('Height')
```