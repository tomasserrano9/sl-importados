const SHEET_ID="1l6pRTYDWOf4--MpL2wf0Pu79VA7dUVsXPoQsm0s6mNI"
const SHEET_NAME="PRODUCTOS"
const WSP="5492326471208"

let products=[]

function formatPrice(n){
return n.toLocaleString("es-AR")
}

async function loadProducts(){

const url=`https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:json&sheet=${SHEET_NAME}`

const res=await fetch(url)
const txt=await res.text()

const json=JSON.parse(txt.match(/setResponse\((.*)\)/)[1])

const rows=json.table.rows

products=[]

rows.forEach(r=>{
const c=r.c

if(!c||!c[1])return

products.push({
name:c[1].v,
category:c[2]?.v||"",
price:c[4]?.v||0,
desc:c[6]?.v||"",
img:c[9]?.v||""
})
})

renderProducts()
}

function renderProducts(){

const grid=document.getElementById("productsGrid")
grid.innerHTML=""

products.forEach(p=>{

const wspMsg=encodeURIComponent(`Hola! Me interesa este producto:\n${p.name}\nPrecio: $${formatPrice(p.price)}`)

const card=document.createElement("div")
card.className="card"

card.innerHTML=`

<img class="card-img" src="${p.img||""}" />

<div class="card-body">

<div class="card-name">${p.name}</div>

<div class="card-price">$${formatPrice(p.price)}</div>

<a class="card-wsp" target="_blank" href="https://wa.me/${WSP}?text=${wspMsg}">

Consultar

</a>

</div>
`

grid.appendChild(card)

})

document.getElementById("productCount").textContent=products.length

}

loadProducts()
