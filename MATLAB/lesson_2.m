Изучение красного смещения звёзд
close all
clear variables

1. Импорт данных
spectra     = importdata("spectra.csv")
starNames   = importdata("star_names.csv");
lambdaStart = importdata("lambda_start.csv");
lambdaDelta = importdata("lambda_delta.csv");

Требуемые константы
lambdaPr     = 656.28;     % nm
speedOfLight = 299792.458; % km\c

2. Определение числа наблюдений и количества звёзд
[numObserv, numStars] = size(spectra);

3. Получение вектора длины волн lambda
lambdaEnd = lambdaStart + (numObserv - 1) * lambdaDelta;
lambda    = (lambdaStart : lambdaDelta : lambdaEnd)';

4. Получение векторов минимальных интенсивностей и их индексов
[spectraStars, indx] = min(spectra);
lambdaStars = lambda(indx);

5. Рассчет скорости движения всех звезд (вектор  speed)
z     = (lambdaStars / lambdaPr) - 1;
speed =  z * speedOfLight;

6. Построение графика спектров всех звёзд
graphStars = figure;

hold on;
for indxGraph = 1 : numStars
    if speed(indxGraph) > 0
        plot(lambda, spectra(:, indxGraph), ...
             '-', ...
             'Linewidth', 3);
    else 
        plot(lambda, spectra(:, indxGraph), ...
             '--', ...
             'Linewidth', 1); 
    end
end
hold off;
7. Добавление на график названия, подписи осей, сетки и легенды
set   (graphStars, 'Visible', 'on'); 
xlabel('Длина волны, нм');
ylabel(['Интенсивность, эрг/см^2/с/', char(197)]);
title ('Спектры звёзд');
text(632, 2.25 * 10^(-13),'Старченко Иван, Б01-005');
legend(starNames);
grid on;
8. Получение вектора movaway
movaway = starNames(speed > 0);

9. Сохранение графика как картини в формате png
saveas(graphStars, 'spectra.png');
