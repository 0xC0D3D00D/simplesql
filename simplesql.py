#!/usr/bin/python
"""
SYNOPSIS
    simplesql [-h,--help] [-v,--verbose] [--version]

    DESCRIPTION
    A simple python client for mysql

    EXIT STATUS
    Zero on a successful exit, One otherwise

    AUTHOR
    Mohammad Hossein Heydari <mdh.heydari@gmail.com>

    LICENSE
    simplesql - A simple python client for mysql
    Copyright (C) 2015 Mohammad Hossein Heydari

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    VERSION
    1.00
"""
import argparse
import cmd
import mysql.connector
import sys

class SqlCommandForwarder(cmd.Cmd):
    """Forward the commands from user to mysql connection"""
    def __init__(self, mysql_connection, verbose):
        cmd.Cmd.__init__(self)
        self.mysql_connection = mysql_connection
        self.verbose = verbose
        self.prompt = "\033[4;32mSQL>\033[0m "

    def default(self, line):
        if line == "q" or line == "quit":
            if self.verbose:
                print "Closing the program..."
            return True

        cursor = self.mysql_connection.cursor()
        try:
            if self.verbose:
                print "Sending query to the server..."
            cursor.execute(line)
            result = cursor.fetchall()
            if self.verbose:
                print "Query executed successfully."

            for atuple in result:
                print atuple
            self.mysql_connection.commit()
        except mysql.connector.errors.ProgrammingError, argument:
            print "\033[1;31mError", argument, "\033[0m"

def main():
    """Main entry point for the script."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("--version", help="show the program version",
                        action="store_true")
    parser.add_argument("-H", "--host", help="mysql server host", type=str,
                        default="localhost")
    parser.add_argument("-P", "--port", help="mysql server port", type=str,
                        default=3306)
    parser.add_argument("-u", "--user", help="mysql username", type=str,
                        default="root")
    parser.add_argument("-p", "--password", help="mysql password", type=str,
                        default="")
    args = parser.parse_args()

    print "simplesql v1.00  Copyright (C) 2015  Mohammad Hossein Heydari"
    print "This program comes with ABSOLUTELY NO WARRANTY."
    print "This is free software, and you are welcome to redistribute it"
    print "under certain conditions."
    if args.version:
        return 0

    connection = None
    try:
        if args.verbose:
            print "Connecting to database..."
        connection = mysql.connector.connect(host=args.host,
                                             port=args.port,
                                             user=args.user,
                                             password=args.password)
        if args.verbose:
            print "Connected."
    except mysql.connector.Error, argument:
        print "\033[1;31mError", argument, "\033[0m"
        return 1

    # start the CLI
    SqlCommandForwarder(connection, args.verbose).cmdloop()

    if args.verbose:
        print "Closing the database connection..."
    connection.close()
    if args.verbose:
        print "Connection closed."

    return 0

if __name__ == "__main__":
    sys.exit(main())
