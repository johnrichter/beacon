import beacon


if __name__ == '__main__':
    args = beacon.parse_arguments()

    located_person = beacon.find_online_presence(
        args.first_name, args.last_name, args.middle_name, args.domains,
        args.linkedin_url, args.angellist_url, args.twitter_url
    )

    print(located_person)
