const yourAddress = '0x7105fbBB3CfA438EDc4D4F92394D09F6E4E55Ae6'
const value = '0xde0b6b3a7640000' // это 1 эфир в hex-е.
const desiredNetwork = '3' // id сети Ropsten

if (typeof window.ethereum === 'undefined') {
    alert('Looks like you need a Dapp browser to get started.')
    alert('Consider installing MetaMask!')

} else {
    ethereum.enable()

        .catch(function (reason) {
            if (reason === 'User rejected provider access') {
                alert('User rejected provider access')
            } else {
                alert('There was an issue signing you in.')
            }
        })

        .then(function (accounts) {
            const account = accounts[0]
            sendEtherFrom(account, function (err, transaction) {
                if (err) {
                    return alert(`There's a problem with your transaction`)
                }

                alert('Transaction is successfully done! Thank you.')
            })

        })
}

function sendEtherFrom(account, callback) {

    const method = 'eth_sendTransaction'

    const parameters = [{
        from: account,
        to: yourAddress,
        value: value,
    }]

    const from = account

    const payload = {
        method: method,
        params: parameters,
        from: from,
    }

    ethereum.sendAsync(payload, function (err, response) {
        const rejected = 'User denied transaction signature.'
        if (response.error && response.error.message.includes(rejected)) {
            return alert(`We can't take your money without your permission.`)
        }

        if (err) {
            return alert('There was an issue, please try again.')
        }

        if (response.result) {
            const txHash = response.result
            alert('Transaction generated but not yet mined! Please wait.')

            pollForCompletion(txHash, callback)
        }
    })
}

function pollForCompletion(txHash, callback) {
    let calledBack = false

    const checkInterval = setInterval(function () {

        const notYet = 'response has no error or result'
        ethereum.sendAsync({
            method: 'eth_getTransactionByHash',
            params: [txHash],
        }, function (err, response) {
            if (calledBack) return
            if (err || response.error) {
                if (err.message.includes(notYet)) {
                    return 'transaction is not yet mined'
                }

                callback(err || response.error)
            }

            const transaction = response.result
            clearInterval(checkInterval)
            calledBack = true
            callback(null, transaction)
        })
    }, 2000)
}
