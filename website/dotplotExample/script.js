function getJson(url) {
    return fetch(url)
        .then(result => result.json())
        .catch(error => {
            console.log(error);})
}
        
function mounted(articles, clusters, quantity) {
    this.getJson('./data.json')
        .then(data => {
            for (let el of data.articles) {
                articles.push(el);
            }
            for (let el of data.clusters) {
                clusters.push(el);
            }
            quantity.push(data.clusterQuantity);
    });
}
        
function makeElement(article) {
    let el = document.createElement('div');
    el.setAttribute('class', 'article');
    let title = document.createElement('p');
    title.textContent = article.title;
    let authors = document.createElement('p');
    authors.textContent = article.authors;
    let doi = document.createElement('a');
    doi.textContent = article.doi;
    doi.href = article.doi;   
    doi.setAttribute('class', 'topicKeyword');
    el.append(title, authors, doi);
    return el;
}
        
function makeList(keyword, classNum) {
    const list = document.createElement('div');
    list.setAttribute('class', 'articleList');
    const filter = document.createElement('p');
    filter.textContent = `Filter by ${keyword}:`;
    filter.setAttribute('class', 'filterArticle');
    list.append(filter);
    for (let article of articles) {
        if (((article.keywords).includes(keyword)) && (article.class === classNum)) {      
            list.append(makeElement(article));   
        } 
    }
    return list;
}
        
function getList() {
    const list = document.querySelector('.articleList');
    const newList = makeList(this.textContent, this.getAttribute('classNum'));
    container.replaceChild(newList, list);
}
        
function getAuthors(article) {
    authors = (article.authors).split(', ');
    if (authors.length > 3) {
        return `${(authors.slice(0, 3)).join(', ')} et al.`;     
    } else return authors.join(', ');
}
        
const colors = ['#0072ce', '#e82727', '#00b140', '#ffa500', '#ffff00'];
const articles = [], clusters = [], quantity = [];
mounted(articles, clusters, quantity);
        
const clNumber = [], clKeywords = [], clWeights = [], clQuantity = [];
const artTitle = [], artAuthors = [], artKeywords = [], artDoi = [], artClass = [];
const container = document.querySelector('div.container');
        
setTimeout(() => {
    for (let cluster of clusters) {
        clNumber.push(cluster.number);
        clKeywords.push((cluster.keywords).split(', '));
        clWeights.push(cluster.weights);
        clQuantity.push(cluster.quantity);
    }
        
    const trace = [];
    for (let i = 0; i < quantity[0]; i++) {
        const dataX = [], dataY = [], dataColor = [], dataName = [];
        for (let article of articles) {
            if (article.class == i) {
                artDoi.push(article.doi);
                dataX.push(article.axisX);
                dataY.push(article.axisY);
                dataColor.push(colors[i]);
                dataName.push(`<b>${article.title}</b><br>${getAuthors(article)}<br><b>DOI: </b>${article.doi}`);
            }
        }
        trace.push({
            hoverinfo: 'text',
            name: '',
            x: dataX,
            y: dataY,
            mode: 'markers',
            textsize: 10,
            text: dataName,
            marker: { size: 8, color: dataColor }
        })};
            
    const layout = {
        title: {
            text: 'Journal articles point diagram',
            font: { family: 'Times New Roman', size: 34, color: 'black' },
        },
        showlegend: false,
        autosize: true,
        xaxis: { showgrid: false, zeroline: false, showticklabels: false },
        yaxis: { showgrid: false, zeroline: false, showticklabels: false }
    };
    const myPlot = document.querySelector('div.content');
    Plotly.newPlot(myPlot, trace, layout);
    myPlot.on('plotly_click', function(data){
        if (data.points.length === 1)
            window.open(artDoi[data.points[0].pointNumber]);
    });  
    const keywords = [];
    for (let i = 0; i < quantity; i++) {
        const voc = {};
        for (let j = 0; j < clKeywords[i].length; j++) {
            voc[clKeywords[i][j]] = clWeights[i][j];
        }
        keywords.push(voc);
    }      
    const wordcloud = document.createElement('div');
    wordcloud.setAttribute('class', 'topics');
    for (let i = 0; i < quantity; i++) {
        const topic = document.createElement('div');
        topic.setAttribute('class', 'topic');
        const topicName = document.createElement('p');
        topicName.textContent = clKeywords[i][0];
        topicName.setAttribute('class', 'topicName');
        topicName.setAttribute('classNum', i);
        topicName.addEventListener('click', getList);
        topicName.style.color = colors[i];
        topicName.style.fontSize = `30px`; 
        topic.append(topicName)
        for (let j = 1; j < clKeywords[i].length; j++) {
            let keyword = document.createElement('p');
            keyword.textContent = clKeywords[i][j];
            keyword.setAttribute('class', 'topicKeyword');
            keyword.setAttribute('classNum', i);
            keyword.addEventListener('click', getList);
            keyword.style.color = colors[i];
            keyword.style.fontSize = `18px`;  
            topic.append(keyword);
        }
        wordcloud.append(topic);
    }
    container.append(wordcloud);
    const artList = document.createElement('div');
    artList.setAttribute('class', 'articleList');
    container.append(artList);
}, 1000);
    