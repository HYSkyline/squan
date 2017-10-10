if (window.screen.width > 767) {
	var infoRowWidth = document.getElementById('infoRow').offsetWidth;
	console.log('infoRowWidth: ' + infoRowWidth + 'px;')

	var avatarContainer = document.getElementById('avatarDiv');
	var infoContainer = document.getElementById('infoDiv');

	var widthPercent = 0.55;
	avatarContainer.style.width = infoRowWidth * widthPercent - 20 + 'px';
	infoContainer.style.width = infoRowWidth * (1 - widthPercent) - 15 + 'px';

	var avatarHeight = avatarContainer.offsetHeight;
	var nameHeight = document.getElementById('nameRow').offsetHeight;
	var mainInfoHeight = document.getElementById('mainInfo').offsetHeight;
	var chartDivElement = document.getElementById('quizChart');
	chartDivElement.style.minHeight = avatarHeight - nameHeight - mainInfoHeight + 14 + 'px';
	chartDivElement.style.top = '-14px';
}