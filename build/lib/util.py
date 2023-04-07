from typing import Tuple
from dotenv import load_dotenv
import datetime
import os
import psycopg2
import time

load_dotenv()

def setup() -> None:
    db         = os.getenv('DB')
    username   = os.getenv('USERNAME')
    server     = os.getenv('SERVER')
    password   = os.getenv('PASSWORD')
    port       = os.getenv('PGPORT')

    return db, username, server, password, port

def addPortfolio(portfolio):
    assert portfolio is not None
    assert portfolio.Name is not None
    assert portfolio.Positions is not None
    assert portfolio.Positions == []

    db, username, server, password, port = setup()

    status = True
    msg = None
    connection=None
    try:
        connection = psycopg2.connect(user=username, password=password, host=server, port=port, database=db)
        cursor = connection.cursor()
        portfolioSQL="INSERT INTO crypto_portfolio(name,positions) VALUES('{}','{}') RETURNING id".format(portfolio.Name, portfolio.Positions)
        cursor.execute(portfdolioSQL)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        if connection:
            connection.rollback()
        msg = "Failed to add new portfolio, error : {}".format(error)
        print(msg)
        status = False

    finally:
        if connection:
            cursor.close()
            connection.close()
    return status, msg

def addSignal(signal):
    assert signal is not None
    assert signal.Exchange is not None
    assert signal.Market is not None
    assert signal.Side is not None
    assert signal.Symbol is not None
    assert signal.Value is not None and signal.Value > 0
    assert signal.Portfolio is not None and signal.Portfolio > 0

    db, username, server, password, port = setup()

    status = True
    msg = None
    connection=None
    try:
        connection = psycopg2.connect(user=username, password=password, host=server, port=port, database=db)
        cursor = connection.cursor()

        signalSQL = "INSERT INTO crypto_signal(symbol, exchange, market, side, value, status, description, portfolio, ts) VALUES('{}','{}','{}','{}','{}','{}','{}','{}',now()) RETURNING id".format(signal.Symbol,signal.Exchange,signal.Market,signal.Side,signal.Value,signal.Status,"Signal for {}:{} to {} {} for Portfolio {}".format(signal.Exchange, signal.Market, signal.Side, signal.Value, signal.Portfolio), signal.Portfolio)
        cursor.execute(signalSQL)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        if connection:
            connection.rollback()
        msg = "Failed to add new Signal based on signal id {}, error : {}".format(signal.SignalId, error)
        print(msg)
        status = False

    finally:
        if connection:
            cursor.close()
            connection.close()
    return status, msg
