%% 3D Tactile Contour Tracing Simulation (Krause et al. 2015, Fig. 4B style)
clf; clear; clc;

% ===== Simulation Parameters =====
params_search = struct('mu', 0.3, 'omega', 1.0, 'gamma', 4.0);   % Search mode
params_sample = struct('mu', 0.007, 'omega', 2.0, 'gamma', 4.0);   % Sampling mode
current_params = params_search;

s_alpha = 0.5;       % Joint velocity scaling (azimuth)
s_beta = 0.5;        % Joint velocity scaling (elevation)
antenna_length = 10; % Antenna length

dt = 0.02;           % Time step
T_sampling = 10.0;   % Sampling duration (sec)
steps_sampling = round(T_sampling / dt);
contact_flag = false;

% ===== Antenna Base Point (change here as desired) =====
base = [-10, 0, -5];  % [X, Y, Z] of the antenna's base

% ===== Initial Hopf oscillator state and antenna pose =====
x = params_search.mu; y = 0;
alpha = 0; beta = 0; % Initial joint angles

% ===== 3D Object (Octahedron) =====
vertices = [1 0 0; -1 0 0; 0 1 0; 0 -1 0; 0 0 1; 0 0 -1] * 5;
faces = [1 3 5; 1 5 4; 1 4 6; 1 6 3; 2 3 6; 2 6 4; 2 4 5; 2 5 3];

% ===== Visualization Setup =====
figure('Color','white');
hold on; axis equal; grid on; view(45,30);
xlim([-15 15]); ylim([-15 15]); zlim([-15 15]);
xlabel('X'); ylabel('Y'); zlabel('Z');
title('3D Tactile Contour Tracing (Krause et al. 2015)','FontWeight','normal');

patch('Faces', faces, 'Vertices', vertices, ...
      'FaceColor', [0.7 0.7 0.7], 'EdgeColor', 'k', 'FaceAlpha', 0.5);

head_radius = 2;
[xs,ys,zs] = sphere(20);
surf(xs*head_radius + base(1), ys*head_radius + base(2), zs*head_radius + base(3), ...
     'FaceColor', [0.1 0.7 0.1], 'EdgeColor', 'none');

antenna = plot3([base(1) base(1)], [base(2) base(2)], [base(3) base(3)+antenna_length], ...
                'g-', 'LineWidth', 2);
trajectory = plot3(base(1), base(2), base(3), 'b-', 'LineWidth', 1);
contacts = scatter3([], [], [], 50, 'r', 'filled');

traj_data = base(:);
contact_points = zeros(3, 0);

% ===== Main Simulation Loop =====
for step = 1:3000
    % Hopf Oscillator update
    r = sqrt(x^2 + y^2);
    dx = current_params.gamma*(current_params.mu^2 - r^2)*x - current_params.omega*y;
    dy = current_params.gamma*(current_params.mu^2 - r^2)*y + current_params.omega*x;
    x = x + dx*dt;
    y = y + dy*dt;

    % Joint angles update
    alpha = alpha + s_alpha*x*dt;
    beta = beta + s_beta*y*dt;
    alpha = mod(alpha, 2*pi);
    beta = max(min(beta, pi/2), -pi/2);

    % Antenna tip position
    tip = base + [antenna_length*cos(alpha)*cos(beta), ...
                  antenna_length*sin(alpha)*cos(beta), ...
                  antenna_length*sin(beta)];

    % --- Continuous Collision Detection (sub-stepping) ---
    n_substeps = 10;
    intersect = false; pt = [0 0 0]; face_idx = 0;
    for s = 1:n_substeps
        interp_tip = base + (s/n_substeps)*(tip-base);
        [sub_hit, sub_pt, sub_face_idx] = rayObjectIntersection(base, interp_tip, vertices, faces);
        if sub_hit
            intersect = true;
            pt = sub_pt;
            tip = interp_tip; % Clamp tip to intersection point
            face_idx = sub_face_idx;
            break;
        end
    end

    % --- Contact Response ---
    if intersect
        if ~contact_flag % New contact event
            current_params = params_sample;
            contact_flag = true;

            % Get surface normal at contact
            normal = getFaceNormal(pt, vertices, faces, face_idx);

            % Push tip slightly out of surface to avoid sticking
            tip = pt + 0.01*normal;

            % 180° phase shift (as in paper)
            x = -x;
            y = -y;

            % Store contact
            contact_points = [contact_points, pt'];
        end
    else
        if contact_flag
            contact_flag = false;
        end

        % Return to search mode after timeout
        if current_params.mu == params_sample.mu
            if step > steps_sampling
                current_params = params_search;
            end
        end
    end

    % --- Visualization update ---
    set(antenna, 'XData', [base(1) tip(1)], 'YData', [base(2) tip(2)], 'ZData', [base(3) tip(3)]);
    traj_data = [traj_data, tip'];
    set(trajectory, 'XData', traj_data(1,:), 'YData', traj_data(2,:), 'ZData', traj_data(3,:));
    set(contacts, 'XData', contact_points(1,:), 'YData', contact_points(2,:), 'ZData', contact_points(3,:));
    drawnow limitrate;
end

%% --- Helper Functions ---

function [intersect, pt, face_idx] = rayObjectIntersection(rayStart, rayEnd, vertices, faces)
    intersect = false; pt = [0 0 0]; face_idx = 0;
    rayDir = rayEnd - rayStart;
    for i = 1:size(faces,1)
        v0 = vertices(faces(i,1),:);
        v1 = vertices(faces(i,2),:);
        v2 = vertices(faces(i,3),:);
        [hit, t] = rayTriangleIntersection(rayStart, rayDir, v0, v1, v2);
        if hit && t <= 1 && t >= 0
            intersect = true;
            pt = rayStart + t*rayDir;
            face_idx = i;
            return;
        end
    end
end

function [hit, t] = rayTriangleIntersection(rayStart, rayDir, v0, v1, v2)
    epsilon = 1e-8;
    edge1 = v1 - v0;
    edge2 = v2 - v0;
    h = cross(rayDir, edge2);
    a = dot(edge1, h);
    if abs(a) < epsilon
        hit = false; t = inf; return;
    end
    f = 1/a;
    s = rayStart - v0;
    u = f * dot(s, h);
    if u < 0 || u > 1
        hit = false; t = inf; return;
    end
    q = cross(s, edge1);
    v = f * dot(rayDir, q);
    if v < 0 || u + v > 1
        hit = false; t = inf; return;
    end
    t = f * dot(edge2, q);
    hit = t > epsilon;
end

function normal = getFaceNormal(pt, vertices, faces, face_idx)
    if face_idx > 0
        v0 = vertices(faces(face_idx,1),:);
        v1 = vertices(faces(face_idx,2),:);
        v2 = vertices(faces(face_idx,3),:);
        normal = cross(v1-v0, v2-v0);
        normal = normal / norm(normal);
    else
        normal = [0 0 1];
    end
end