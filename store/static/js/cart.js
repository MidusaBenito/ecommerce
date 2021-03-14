var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var sandleId = this.dataset.sandle
		var sizeId = this.dataset.size
		var action = this.dataset.action
		var sandleDetails = [sandleId, sizeId]
		//console.log('sandleId:', sandleId, 'Action:', action)
		//console.log('USER:', user)
		//console.log('SandleDetails:', sandleDetails)

		if (user == 'AnonymousUser'){
			addCookieItem(sandleDetails, action)
		}else{
			updateUserOrder(sandleId, sizeId, action)
		}
	})
}

function updateUserOrder(sandleId, sizeId, action){
	//console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'sandleId':sandleId, 'sizeId':sizeId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(sandleDetails, action){
	//console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[sandleDetails] == undefined){
		cart[sandleDetails] = {'quantity':1}

		}else{
			cart[sandleDetails]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[sandleDetails]['quantity'] -= 1

		if (cart[sandleDetails]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[sandleDetails];
		}
    }
    //console.log('Cart:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}