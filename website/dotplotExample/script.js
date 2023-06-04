function getJson(url) {
    return fetch(url)
        .then(result => result.json())
        .catch(error => {
            console.log(error);
        });
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

const articles = [], clusters = [], quantity = [];
mounted(articles, clusters, quantity);
const clNumber = [], clKeywords = [], clQuantity = [];
setTimeout(() => {
    for (let cluster of clusters) {
        clNumber.push(cluster.number);
        clKeywords.push((cluster.keywords).split(', '));
        clQuantity.push(cluster.quantity);
}
    const contents = document.querySelector('div.content');
    for (let i = 0; i < quantity[0]; i++) {
        let classContent = document.createElement('div');
        classContent.setAttribute('class', 'classContent');
        let classHeader = document.createElement('h3');  
        let classLink = document.createElement('a');
        let className = (clKeywords[i][0])[0].toUpperCase() + (clKeywords[i][0]).slice(1);
        classLink.textContent = className;
        classLink.href = `#Class${i}`;
        classHeader.append(classLink);
        classContent.append(classHeader);
        let classKeywords = document.createElement('p');
        classKeywords.textContent = `Keywords: ${((clKeywords[i]).slice(1)).join(', ')}`;
        classContent.append(classKeywords);   
        let classQuantity = document.createElement('p');
        classQuantity.textContent = `Quantity of articles: ${clQuantity[i]}`;
        classContent.append(classQuantity);   
        contents.append(classContent);
    }
    const classes = document.querySelector('div.container');
    for (let i = 0; i < quantity[0]; i++) {
        let classArticle = document.createElement('div');   
        classArticle.setAttribute('class', 'articleList');
        let classHeader = document.createElement(`h3`);  
        classHeader.setAttribute('id', `Class${i}`);
        let className = (clKeywords[i][0])[0].toUpperCase() + (clKeywords[i][0]).slice(1);
        classHeader.textContent = className;
        classArticle.append(classHeader);  
        let articleList = document.createElement('div');
        articleList.setAttribute('class', 'articles');
        for (let article of articles) {
            if (article.class == i) {
                let articleDiv = document.createElement('div');   
                if (articleList.children.length >= 5) {
                    articleDiv.setAttribute('class', 'article disable');
                } else {
                    articleDiv.setAttribute('class', 'article');
                }                       
                let title = document.createElement('h4');
                let nameLink = document.createElement('a');
                nameLink.textContent = article.title;
                nameLink.href = article.doi;
                title.append(nameLink);
                articleDiv.append(title);
                let authors = document.createElement('p');
                authors.textContent = article.authors;
                authors.setAttribute('class', 'data');
                articleDiv.append(authors);
                let articleLink = document.createElement('div');
                articleLink.setAttribute('class', 'articleLink');
                articleLink.append('DOI: ')
                let link = document.createElement('a');
                link.setAttribute('class', 'doiLink');
                link.textContent = article.doi;
                link.href = article.doi;           
                articleLink.append(link);
                articleDiv.append(articleLink);
                articleList.append(articleDiv);
            }
        }       

        let btnMore = document.createElement('button');
        btnMore.setAttribute('class', 'btnMore');
        btnMore.textContent = "Show more";
        btnMore.addEventListener("click", () => {
            let list = btnMore.parentElement.querySelector('.articles');
            if (list.children.length > 6) {
                for (let i = 6; i < list.children.length; i++) {
                    list.childNodes[i].classList.toggle('disable');
                }
            }
            if (btnMore.textContent == 'Show more') {
                btnMore.textContent = 'Hide';
            } else {
                btnMore.textContent = "Show more";
            }
        });
        classArticle.append(articleList);
        classArticle.append(btnMore);
        classes.appendChild(classArticle);
    }   
}, 1000);
    